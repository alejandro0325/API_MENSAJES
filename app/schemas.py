from pydantic import BaseModel, Field
from pydantic import ConfigDict
from datetime import datetime
from typing import Dict

class MensajeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str = Field(..., pattern="^(user|system)$")

class MensajeCrear(MensajeBase):
    pass

class MensajeRespuesta(MensajeBase):
    metadata: Dict

#parametrizacion del esquema del mensaje a ingresar



