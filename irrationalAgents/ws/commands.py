from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import ConnectionManager
import json
from handler import *
import uvicorn

app = FastAPI()

manager = ConnectionManager()


@app.websocket("/ative")
async def action_chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
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