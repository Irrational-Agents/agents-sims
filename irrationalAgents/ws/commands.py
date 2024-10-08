'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2024-09-21 16:03:17
LastEditors: ephie && ephiewangyf@gmail.com
<<<<<<< HEAD
LastEditTime: 2024-10-06 13:57:17
=======
LastEditTime: 2024-09-21 16:05:35
>>>>>>> origin/sims-setup
FilePath: /Agents-Sim/irrationalAgents/ws/commands.py
Description: 
'''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import ConnectionManager
<<<<<<< HEAD
import json
from handler import *
import uvicorn
=======
>>>>>>> origin/sims-setup

app = FastAPI()

manager = ConnectionManager()

<<<<<<< HEAD

@app.websocket("/ative")
async def action_chat(websocket: WebSocket):
=======
@app.websocket("/act")
async def websocket_endpoint(websocket: WebSocket):
>>>>>>> origin/sims-setup
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
<<<<<<< HEAD
            data =json.loads(data)
            handle_active(data.get("agents"))
            filtered_items = filter(lambda item: item[1] is not None, AGENT_DICT.items())
            actived_agents = [agent for agent, _ in filtered_items]
            await manager.send_message(f"success: {actived_agents}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message("Bye!!!",websocket)

@app.websocket("/chat")
async def action_chat(websocket: WebSocket):

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data =json.loads(data)
            resp = handle_chat(data)
            await manager.send_message(resp,websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message("Bye!!!",websocket)


if __name__ == '__main__':
    uvicorn.run('commands:app')
=======
            await manager.send_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message("Bye!!!",websocket)
>>>>>>> origin/sims-setup
