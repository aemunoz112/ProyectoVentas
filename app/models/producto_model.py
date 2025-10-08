from pydantic import BaseModel
from datetime import datetime

class Producto(BaseModel):
    sku: str
    nombre: str
    tipo: str
    dim_largo: float
    dim_diametro: float
    ancho: float
    espesor: float
    peso_teorico_per_unit: float
    unidad_medida: str
    usos: str
    stock: int
    

class ProductoCreate(Producto):
    pass

class ProductoResponse(Producto):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True