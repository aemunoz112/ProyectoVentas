from pydantic import BaseModel
from datetime import datetime

class RolModuloPermisoBase(BaseModel):
    rol_id: int
    modulo_id: int
    permiso_id: int
    permitido: bool = False

class RolModuloPermisoCreate(RolModuloPermisoBase):
    pass

class RolModuloPermisoResponse(RolModuloPermisoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
