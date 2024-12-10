from typing import Optional, Dict
from logger_config import setup_logger

logger = setup_logger('API-client-handler')


class AgentClient:
    def __init__(self, ws_client):
        self.ws_client = ws_client

    # Building 相关API
    async def get_building_info(self, building_id: int) -> Dict:
        """获取建筑信息"""
        return await self.ws_client.send_command(
            "command.building.GetBuildingInfo",
            {"buildingID": building_id}
        )

    async def get_buildings(self) -> Dict:
        """获取所有建筑"""
        return await self.ws_client.send_command(
            "command.building.GetBuildings"
        )

    # Chat 相关API
    async def npc_chat_update(self) -> None:
        """更新NPC聊天气泡"""
        return await self.ws_client.send_command(
            "command.chat.NPCChatUpdate"
        )

    # Config 相关API
    async def get_buildings_config(self) -> Dict:
        """获取建筑配置"""
        return await self.ws_client.send_command(
            "command.config.GetBuildingsConfig"
        )

    async def get_equipments_config(self) -> Dict:
        """获取装备配置"""
        return await self.ws_client.send_command(
            "command.config.GetEquipmentsConfig"
        )

    async def get_npcs_config(self) -> Dict:
        """获取NPC配置"""
        return await self.ws_client.send_command(
            "command.config.GetNPCsConfig"
        )

    # Map 相关API
    async def get_map_scene(self) -> Dict:
        """获取地图场景"""
        return await self.ws_client.send_command(
            "command.map.GetMapScene"
        )

    async def get_map_town(self) -> Dict:
        """获取城镇地图"""
        return await self.ws_client.send_command(
            "command.map.GetMapTown"
        )

    async def npc_navigate(self, npc_id: int, x: int, y: int) -> None:
        """NPC导航"""
        return await self.ws_client.send_command(
            "command.map.NPCNavigate",
            {
                "npc_id": npc_id,
                "x": x,
                "y": y
            }
        )

    async def npc_navigate_time(self, npc_id: int, x: int, y: int) -> Dict:
        """计算NPC导航时间"""
        return await self.ws_client.send_command(
            "command.map.NPCNavigateTime",
            {
                "npc_id": npc_id,
                "x": x,
                "y": y
            }
        )

    # NPC 相关API
    async def get_npc_info(self, npc_id: int) -> Dict:
        """获取NPC信息"""
        return await self.ws_client.send_command(
            "command.npc.GetNPCInfo",
            {"NPCID": npc_id}
        )

    async def get_npcs(self) -> Dict:
        """获取所有NPC"""
        return await self.ws_client.send_command(
            "command.npc.GetNPCs"
        )

    # Player 相关API
    async def get_player_info(self) -> Dict:
        """获取玩家信息"""
        return await self.ws_client.send_command(
            "command.player.GetPlayerInfo"
        )

