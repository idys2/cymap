from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schema import MetricSchema, MetricSchemaCreate
from database.model import Metric as MetricModel
from database.session import get_db_session
from api.auth import azure_scheme

router = APIRouter(
    dependencies=[Security(azure_scheme)]
)

# create metric
@router.post("/metric", response_model=MetricSchema)
async def create_metric(metric: MetricSchemaCreate, db: AsyncSession = Depends(get_db_session)):
    metric = await MetricModel.create(db, **metric.model_dump())
    return metric

# read metric from id
@router.get("/metric/{uuid}", response_model=MetricSchema)
async def get_metric(id: str, db: AsyncSession = Depends(get_db_session)):
    metric = await MetricModel.get(db, id)
    if not metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return metric

# read all metrics
@router.get("/metrics", response_model=list[MetricSchema])
async def get_all_metrics(db: AsyncSession = Depends(get_db_session)):
    metrics = await MetricModel.get_all(db)
    return metrics

# delete metric
@router.delete("/metric/{uuid}", response_model=MetricSchema)
async def delete_metric(id: str, db: AsyncSession = Depends(get_db_session)):
    metric = await MetricModel.delete(db, id)
    if not metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return metric
