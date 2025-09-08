from sqlalchemy import Column, String, DateTime, Text
from .database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(String)
    timestamp = Column(DateTime)
    sender = Column(String)
    metadata_json = Column("metadata", Text, nullable=True)

# tipos de datos en los campos del mensaje, se crea la tabla "mensajes" con sus columnas




