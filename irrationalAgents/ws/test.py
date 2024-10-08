from fastapi.testclient import TestClient

from commands import app
def test_active():
    client = TestClient(app)
    with client.websocket_connect("/active") as websocket:
        websocket.send_json({"agents": ["zhang_san"]})
        data = websocket.receive_json()
        assert data == {"success":["zhang_san"]}


def test_read_main():
    client = TestClient(app)
    with client.websocket_connect("/chat") as websocket:
        websocket.send_json({"agent": "zhang_san"
                             ""})
        data = websocket.receive_json()
        assert data == {"success":["zhang_san"]}
