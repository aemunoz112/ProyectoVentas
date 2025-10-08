from pydantic import BaseModel
from datetime import datetime

class AtributoBasemodel(BaseModel):
    nombre: str
    tipo_dato: str     # texto, numero, booleano, fecha, json
    descripcion: str
    es_requerido: bool

class AtributoCreated(AtributoBasemodel):
    pass

class AtributoResponse(AtributoBasemodel):
    id: int
    created_at: datetime
    updated_at: datetime
