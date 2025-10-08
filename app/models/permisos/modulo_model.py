from pydantic import BaseModel
from datetime import datetime

class ModuloBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    ruta: str | None = None

class ModuloCreate(ModuloBase):
    pass

class ModuloResponse(ModuloBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
