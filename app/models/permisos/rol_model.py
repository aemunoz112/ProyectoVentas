from pydantic import BaseModel
from datetime import datetime

class RolBase(BaseModel):
    nombre: str
    descripcion: str

class RolResponse(RolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
