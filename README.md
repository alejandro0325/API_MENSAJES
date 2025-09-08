#  Proyecto: Mensajes API

## Este proyecto desarrolla una API REST para la gestion de mensajes en sesiones de usuario 

Facilita la creación, el procesamiento y la recuperación de mensajes que se encuentran en una base de datos SQLite

Características fundamentales: - Comprobación de datos mediante Pydantic. 
-Gestion de mensajes con metadatos automaticos (numero de palabras, caracteres, timestamp).
-Filtrado de contenido no adecuado a través de un catálogo de términos prohibidos. 
-Persistencia utilizando SQLAlchemy y SQLite. 
-Documentación automatizada con Swagger UI.
-Test unitarias con pytest.

# Instrucciones para la configuracion

1. Clonar repositorio.
2. Crear un entorno virtual.
3. Instalar dependecias del archivo: pip install -r requirements.txt
4. Ejecutar la API con: uvicorn app.main:app --reload
5. la API estara disponible en http://127.0.0.1:8000

# DOCUMENTACIÓN

POST /api/mensajes
ENDPOINT: http://127.0.0.1:8000/api/mensajes
ejm del JSON para crear el mensaje:
{
  "message_id": "msg-1",
  "session_id": "sesion-1",
  "content": "Hola mundo",
  "timestamp": "2025-09-07",
  "sender": "user"
}

ejm response:

{
    "message_id": "msg-3",
    "session_id": "sesion-1",
    "content": "prueba 2",
    "timestamp": "2025-09-07T00:00:00",
    "sender": "user",
    "metadata": {
        "conteo_palabras": 2,
        "conteo_caracteres": 8,
        "procesado_en": "2025-09-08T02:53:37.435166"
    }
}
-Si se va ingresar una palabra prohibida el response debe devolver mensaje spam

Endpoint para listar mensajes:
GET /api/mensajes/{session_id}
http://127.0.0.1:8000/api/mensajes/sesion-1

ejm de response:
  {
        "message_id": "msg-1",
        "session_id": "sesion-1",
        "content": "prueba",
        "timestamp": "2025-09-07T15:00:00",
        "sender": "user",
        "metadata": {
            "conteo_palabras": 1,
            "conteo_caracteres": 6,
            "procesado_en": "2025-09-08T01:27:31.222548"
        }
    }


# INSTRUCCIONES PARA PRUEBAS

Para ejecutar las pruebas con: pytest -v

EJM de salida:

tests/test_api.py::test_crear_mensaje_exitoso PASSED
tests/test_api.py::test_crear_mensaje_con_palabra_prohibida PASSED
tests/test_api.py::test_listar_mensajes_por_sesion PASSED
tests/test_api.py::test_filtrar_por_remitente PASSED



