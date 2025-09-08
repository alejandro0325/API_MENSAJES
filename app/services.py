from datetime import datetime
from fastapi import HTTPException
from .schemas import MensajeCrear, MensajeRespuesta

#palabras prohibidas
PALABRAS_PROHIBIDAS = {"spam", "ofensivo", "maldicion"}

def procesar_mensaje(mensaje: MensajeCrear) -> MensajeRespuesta:
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra.lower() in mensaje.content.lower():
            raise HTTPException(status_code=400, detail=f"El mensaje contiene una palabra prohibida: '{palabra}'")

    metadatos = {
        "conteo_palabras": len(mensaje.content.split()),
        "conteo_caracteres": len(mensaje.content),
        "procesado_en": datetime.utcnow().isoformat()
    }
    return MensajeRespuesta(**mensaje.dict(), metadata=metadatos)





