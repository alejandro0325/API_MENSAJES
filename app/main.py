from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud, services
from .database import motor, Base, obtener_sesion
import json

Base.metadata.create_all(bind=motor)

app = FastAPI(title="API de Mensajes de Chat (debug)")

@app.post("/api/mensajes", response_model=schemas.MensajeRespuesta)
def crear_mensaje_endpoint(mensaje: schemas.MensajeCrear, db: Session = Depends(obtener_sesion)):
    try:
        procesado = services.procesar_mensaje(mensaje)
        creado = crud.crear_mensaje(db, procesado)
        meta = creado.metadata_json or "{}"
        try:
            meta_obj = json.loads(meta)
        except Exception:
            meta_obj = {}
        return schemas.MensajeRespuesta(
            message_id=creado.message_id,
            session_id=creado.session_id,
            content=creado.content,
            timestamp=creado.timestamp,
            sender=creado.sender,
            metadata=meta_obj,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/mensajes/{id_sesion}", response_model=list[schemas.MensajeRespuesta])
def obtener_mensajes_endpoint(
    id_sesion: str,
    saltar: int = Query(0, ge=0),
    limite: int = Query(10, ge=1, le=100),
    remitente: str | None = Query(None, pattern="^(user|system)?$"),
    db: Session = Depends(obtener_sesion)
):
    registros = crud.obtener_mensajes(db, id_sesion, saltar, limite, remitente)
    resultados = []
    for r in registros:
        try:
            meta = json.loads(r.metadata_json) if r.metadata_json else {}
        except Exception:
            meta = {}
        resultados.append(
            schemas.MensajeRespuesta(
                message_id=r.message_id,
                session_id=r.session_id,
                content=r.content,
                timestamp=r.timestamp,
                sender=r.sender,
                metadata=meta,
            )
        )
    return resultados

# parametrizacion de las rutas que se dan al usuario POST Y GET

