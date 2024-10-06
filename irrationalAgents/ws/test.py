'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2024-10-06 11:48:09
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2024-10-06 12:16:48
FilePath: /Agents-Sim/irrationalAgents/ws/test.py
Description: Test only for develop
'''

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
