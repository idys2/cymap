from uuid import uuid4
from datetime import datetime

from sqlalchemy import DateTime, Text, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import Base


class Metric(Base):
    __tablename__ = 'metrics'
    __table_args__ = ({
        'timescaledb_hypertable': {
            'time_column_name': 'timestamp'
        }
    })

    id: Mapped[str] = mapped_column(Text, nullable=False, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    type_id: Mapped[int] = mapped_column(nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        if not id:
            id = uuid4().hex
        
        transaction = cls(id=id, **kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction
    
    @classmethod
    async def get(cls, db: AsyncSession, id):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction
    
    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def delete(cls, db: AsyncSession, id):
        transaction = await cls.get(db, id)
        if transaction:
            await db.delete(transaction)
            await db.commit()
            return transaction
        else:
            return None
