from datetime import datetime

from pydantic import BaseModel

class MetricSchemaBase(BaseModel):
    timestamp: datetime
    type_id: int
    value: float
    
class MetricSchemaCreate(MetricSchemaBase):
    pass

class MetricSchema(MetricSchemaBase):
    id: str

    class Config:
        from_attributes = True