from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas
import json

def crear_mensaje(db: Session, mensaje: schemas.MensajeRespuesta):
    # debug
    print("DEBUG: metadata que llega a CRUD", repr(mensaje.metadata), type(mensaje.metadata))

    metadata_serializada = json.dumps(mensaje.metadata, ensure_ascii=False)

    db_msg = models.Mensaje(
        message_id=mensaje.message_id,
        session_id=mensaje.session_id,
        content=mensaje.content,
        timestamp=mensaje.timestamp,
        sender=mensaje.sender,
        metadata_json=metadata_serializada,
    )
    db.add(db_msg)
    try:
        db.commit()
        db.refresh(db_msg)
        # debug
        print("DEBUG: metadata guardada", db_msg.metadata_json)
        return db_msg
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El message_id ya existe. Debe ser unico.")

def obtener_mensajes(db: Session, id_sesion: str, saltar: int = 0, limite: int = 10, remitente: str | None = None):
    print("DEBUG: buscando mensajes con session_id =", id_sesion)
    consulta = db.query(models.Mensaje).filter(models.Mensaje.session_id == id_sesion)
    if remitente:
        consulta = consulta.filter(models.Mensaje.sender == remitente)
    resultados = consulta.offset(saltar).limit(limite).all()
    print("DEBUG: encontrados =", len(resultados))
    return resultados

# aqui se maneja todas la peticiones a la DB que son crear y listar, se maneja un DEBUG por unos errores inicales en la insercion de la metadata
    



