import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_mensaje_exitoso():
    data = {
        "message_id": "test-1",
        "session_id": "sesion-test",
        "content": "Hola mundo desde prueba",
        "timestamp": "2025-09-06T15:00:00Z",
        "sender": "user"
    }
    response = client.post("/api/mensajes", json=data)
    assert response.status_code == 200
    body = response.json()
    assert body["message_id"] == "test-1"
    assert "metadata" in body
    assert body["metadata"]["conteo_palabras"] == 4

def test_crear_mensaje_con_palabra_prohibida():
    data = {
        "message_id": "test-2",
        "session_id": "sesion-test",
        "content": "Esto es spam",
        "timestamp": "2025-09-06T15:05:00Z",
        "sender": "user"
    }
    response = client.post("/api/mensajes", json=data)
    assert response.status_code == 400
    assert "palabra prohibida" in response.json()["detail"]

def test_listar_mensajes_por_sesion():
    # insertar mensaje valido
    data = {
        "message_id": "test-3",
        "session_id": "sesion-test",
        "content": "Otro mensaje válido",
        "timestamp": "2025-09-06T15:10:00Z",
        "sender": "system"
    }
    client.post("/api/mensajes", json=data)

    #listar por session_id
    response = client.get("/api/mensajes/sesion-test")
    assert response.status_code == 200
    mensajes = response.json()
    assert any(m["message_id"] == "test-3" for m in mensajes)

def test_filtrar_por_remitente():
    response = client.get("/api/mensajes/sesion-test?remitente=system")
    assert response.status_code == 200
    mensajes = response.json()
    assert all(m["sender"] == "system" for m in mensajes)

