from pydantic import BaseModel
from datetime import datetime

class Orden_ProduccionBasemodel(BaseModel):
    pedido_id: str
    fecha_inicio: str
    fecha_fin_estimada: str
    estado: str
    

class Orden_ProduccionCreated(Orden_ProduccionBasemodel):
    pass

class Orden_ProduccionResponse(Orden_ProduccionBasemodel):
    id: int
    created_at:datetime
    updated_at: datetime