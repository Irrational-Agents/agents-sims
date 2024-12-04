import aiohttp
from typing import Optional
import json
from logger_config import setup_logger
from config import *
import asyncio
import json
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from API.client.handler import AgentClient

logger = setup_logger('API-Client')


class WSClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.is_connected = False
        self.message_handlers = {}
        self.response_futures = {}
        self.reconnect_interval = 5

    async def connect(self):
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect(
                self.uri,
                heartbeat=30.0,
                timeout=60.0
            )
            self.is_connected = True
            logger.info("WebSocket connected to %s", self.uri)
            asyncio.create_task(self._message_loop())
        except Exception as e:
            logger.error("Connection failed: %s", str(e))
            self.is_connected = False
            await self.reconnect()

    async def reconnect(self):
        while not self.is_connected:
            logger.info("Attempting to reconnect in %s seconds...", self.reconnect_interval)
            await asyncio.sleep(self.reconnect_interval)
            await self.connect()

    async def _message_loop(self):
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await self._handle_message(msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error("WebSocket error: %s", str(msg.data))
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.warning("WebSocket connection closed")
                    break
        except Exception as e:
            logger.error("Error in message loop: %s", str(e))
        finally:
            self.is_connected = False
            await self.reconnect()

    async def _handle_message(self, message: str):
        try:
            data = json.loads(message)
            logger.debug("Received message: %s", data)
            if "request_id" in data:
                future = self.response_futures.get(data["request_id"])
                if future and not future.done():
                    future.set_result(data)
            elif "event" in data:
                handler = self.message_handlers.get(data["event"])
                if handler:
                    await handler(data)
        except Exception as e:
            logger.error("Error handling message: %s", str(e))

    async def send_command(self, command: str, params: Dict = None, timeout: int = 10) -> Dict:
        if not self.is_connected or self.ws is None:
            raise ConnectionError("WebSocket is not connected")

        request_id = f"{command}_{datetime.now().timestamp()}"
        message = {
            "command": command,
            "parameters": params or {},
            "request_id": request_id
        }

        future = asyncio.Future()
        self.response_futures[request_id] = future

        try:
            await self.ws.send_json(message)
            response = await asyncio.wait_for(future, timeout)
            return response
        except asyncio.TimeoutError:
            logger.error("Command timeout: %s", command)
            raise TimeoutError(f"Command {command} timeout")
        finally:
            self.response_futures.pop(request_id, None)

    def register_handler(self, event: str, handler: Callable):
        self.message_handlers[event] = handler

    async def close(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
        self.is_connected = False

async def main():
    # 创建客户端实例
    ws_client = WSClient(ws_url)
    agent_client = AgentClient(ws_client)

    async def on_npc_status_change(data):
        logger.info("NPC status changed: %s", data)
    ws_client.register_handler("npc_status_change", on_npc_status_change)

    try:
        await ws_client.connect()

        buildings = await agent_client.get_buildings()
        logger.info("Buildings: %s", buildings)

        npcs = await agent_client.get_npcs()
        logger.info("NPCs: %s", npcs)

        await asyncio.sleep(3600)

    except Exception as e:
        logger.error("Error: %s", str(e))
    finally:
        await ws_client.close()

if __name__ == "__main__":
    asyncio.run(main())