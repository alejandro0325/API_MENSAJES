from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_BASE_DATOS = "sqlite:///./messages.db"

#ver el SQL ejecutado
motor = create_engine(
    URL_BASE_DATOS,
    echo=True,
    connect_args={"check_same_thread": False}
)

SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)
Base = declarative_base()

def obtener_sesion():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()


