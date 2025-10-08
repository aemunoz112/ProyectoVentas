from pydantic import BaseModel
from datetime import datetime

class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    email: str
    telefono: str
    password: str
    rol_id: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int
    nombres: str
    apellidos: str
    email: str
    telefono: str
    rol_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True