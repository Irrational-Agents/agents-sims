'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2024-09-21 16:02:18
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2024-09-21 16:06:11
FilePath: /Agents-Sim/irrationalAgents/ws/manager.py
Description: 
'''
from fastapi import WebSocket

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)