from pydantic import BaseModel
from datetime import datetime

class PermisoBase(BaseModel):
    nombre: str

class PermisoCreate(PermisoBase):
    pass

class PermisoResponse(PermisoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
