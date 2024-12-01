import aiohttp
from typing import Optional
import json
from logger_config import setup_logger
from config import *
import asyncio
import json
from typing import Dict, Any, Optional, Callable
from datetime import datetime

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
        """建立WebSocket连接"""
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
            # 启动消息接收循环
            asyncio.create_task(self._message_loop())
        except Exception as e:
            logger.error("Connection failed: %s", str(e))
            self.is_connected = False
            await self.reconnect()

    async def reconnect(self):
        """重连机制"""
        while not self.is_connected:
            logger.info("Attempting to reconnect in %s seconds...", self.reconnect_interval)
            await asyncio.sleep(self.reconnect_interval)
            await self.connect()

    async def _message_loop(self):
        """消息接收循环"""
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
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            logger.debug("Received message: %s", data)
            # 处理响应
            if "request_id" in data:
                future = self.response_futures.get(data["request_id"])
                if future and not future.done():
                    future.set_result(data)
            # 处理事件
            elif "event" in data:
                handler = self.message_handlers.get(data["event"])
                if handler:
                    await handler(data)
        except Exception as e:
            logger.error("Error handling message: %s", str(e))

    async def send_command(self, command: str, params: Dict = None, timeout: int = 10) -> Dict:
        """发送命令并等待响应"""
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
        """注册事件处理器"""
        self.message_handlers[event] = handler

    async def close(self):
        """关闭连接"""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
        self.is_connected = False

class GameClient:
    """游戏客户端API封装"""
    def __init__(self, ws_client: WSClient):
        self.ws_client = ws_client

    # 建筑相关API
    async def get_building_info(self, building_id: int) -> Dict:
        return await self.ws_client.send_command(
            "command.building.GetBuildingInfo",
            {"buildingID": building_id}
        )

    async def get_buildings(self) -> Dict:
        return await self.ws_client.send_command("command.building.GetBuildings")

    # NPC相关API
    async def get_npc_info(self, npc_id: int) -> Dict:
        return await self.ws_client.send_command(
            "command.npc.GetNPCInfo",
            {"NPCID": npc_id}
        )

    async def get_npcs(self) -> Dict:
        return await self.ws_client.send_command("command.npc.GetNPCs")

    # 地图相关API
    async def get_map_scene(self) -> Dict:
        return await self.ws_client.send_command("command.map.GetMapScene")

    async def get_map_town(self) -> Dict:
        return await self.ws_client.send_command("command.map.GetMapTown")

async def main():
    # 创建客户端实例
    ws_client = WSClient("ws://localhost:8765")
    game_client = GameClient(ws_client)

    # 注册事件处理器示例
    async def on_npc_status_change(data):
        logger.info("NPC status changed: %s", data)
    ws_client.register_handler("npc_status_change", on_npc_status_change)

    try:
        # 连接服务器
        await ws_client.connect()

        # API调用示例
        buildings = await game_client.get_buildings()
        logger.info("Buildings: %s", buildings)

        npcs = await game_client.get_npcs()
        logger.info("NPCs: %s", npcs)

        # 保持运行一段时间
        await asyncio.sleep(3600)

    except Exception as e:
        logger.error("Error: %s", str(e))
    finally:
        await ws_client.close()

if __name__ == "__main__":
    asyncio.run(main())