'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2024-09-21 16:03:17
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2024-09-21 16:05:35
FilePath: /Agents-Sim/irrationalAgents/ws/commands.py
Description: 
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

@app.websocket("/act")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message("Bye!!!",websocket)