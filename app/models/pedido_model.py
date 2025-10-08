from pydantic import BaseModel
from datetime import datetime

class PedidoBase(BaseModel):
    usuario_id: str
    estado: str
    fecha_entrega_estimada: str
    created_at: str
    updated_at: str

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True