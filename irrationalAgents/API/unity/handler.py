# handlers.py
import os
import json
from typing import Dict, Any
from datetime import datetime
from logger_config import setup_logger
from API.unity.models import *
from config import *
from common_method import *

logger = setup_logger('API-unity-handler')

def gen_agent_by_name(name):
    root_dir = os.path.join(WORK_DIR,f'../storage/sample_data/agents/{name}')
    if not os.path.exists(root_dir):
        logger.error(f"agent {name} not exists!")
        return None
    
    with open(os.path.join(root_dir, "basic_info.json"), 'r', encoding='utf-8') as f:
        basic_info = json.load(f)
    with open(os.path.join(root_dir, "memory/short_term.json"), 'r', encoding='utf-8') as f:
        short_mem = json.load(f)
    return basic_info, short_mem

class UnityHandlers:
    def __init__(self):
        self.NPC_STORAGE_BASE_PATH = os.path.join(WORK_DIR, "../storage/sample_data")
        # 游戏状态存储
        self.players = {}
        self.npcs = {}
        self.map_data = {
            'town': {'name': 'Test Town', 'size': {'width': 1000, 'height': 1000}},
            'scene': {'name': 'Test Scene', 'objects': []}
        }
        self.configs = {
            'equipments': {'weapons': [], 'armors': []},
            'buildings': {'houses': [], 'shops': []}
        }

    def handle_get_npcs(self, params: Dict) -> Dict:
        """Handle request to get all NPCs"""
        try:
            request = NPCGetRequest(**params)
            
            with open(os.path.join(self.NPC_STORAGE_BASE_PATH, "meta.json"), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if request.names:
                logger.info(f"Received get request for NPCs: {request.names}")
                # 检查NPCs是否存在
                valid_npcs = []
                invalid_npcs = []
                for name in request.names:
                    if convert_id2name(name) in data["agents_list"]:
                        valid_npcs.append(name)
                    else:
                        invalid_npcs.append(name)
                
                if not valid_npcs:
                    return {'error': f"No valid NPCs found. Invalid NPCs: {invalid_npcs}"}
                
                if invalid_npcs:
                    logger.warning(f"Skipping invalid NPCs: {invalid_npcs}")
            else:
                valid_npcs = [convert_name2id(name) for name in data["agents_list"]] 
            # 获取NPC信息
            npcs = []
            for npc_id in valid_npcs:
                agent, status = gen_agent_by_name(npc_id)
                if request.isDetails:
                    npc_data = NPCModel(**agent)
                    npc_data.status = status
                else:
                    npc_data = NPCInfoModel(**(agent|status))
                npcs.append(npc_data)
            return {
                'npcs': [npc.model_dump() for npc in npcs] or None
            }
            
        except Exception as e:
            logger.error(f"Error getting NPCs: {str(e)}")
            return {'error': str(e)}

    def handle_get_npc_info(self, params: Dict) -> Dict:
        """Handle request to get specific NPC info"""
        try:
            npc_id = params.get('NPCID')
            
            with open(os.path.join(self.NPC_STORAGE_BASE_PATH, "meta.json"), 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if convert_id2name(npc_id) not in data["agents_list"]:
                logger.warning(f'NPC {npc_id} not found')
                return {'error': f"NPC '{npc_id}' not found"}
            
            agent, status = gen_agent_by_name(npc_id)
            logger.debug(f"get agent {agent}")
            npc_data = NPCModel(**agent)
            npc_data.status = status
            
            return {'npc': npc_data.model_dump()}
            
        except Exception as e:
            logger.error(f"Error getting NPC info: {str(e)}")
            return {'error': str(e)}


    def handle_get_player_info(self, params: Dict) -> Dict:
        """处理获取玩家信息的请求"""
        player_id = params.get('playerID', '')
        return {
            'player': self.players.get(player_id, {
                'id': player_id,
                'name': f'Player_{player_id}',
                'level': 1
            })
        }

    def handle_npc_navigate(self, params: Dict) -> Dict:
        """处理NPC导航请求"""
        try:
            npc_id = params.get('npc_id')
            x = params.get('x')
            y = params.get('y')
            
            if npc_id in self.npcs:
                self.npcs[npc_id]['position'] = {'x': x, 'y': y}
            
            return {'success': True}
        except Exception as e:
            logger.error(f"Error in NPC navigation: {str(e)}")
            return {'error': str(e)}

    def handle_get_map_town(self, params: Dict) -> Dict:
        """处理获取城镇地图的请求"""
        return {'town': self.map_data['town']}

    def handle_get_map_scene(self, params: Dict) -> Dict:
        """处理获取场景地图的请求"""
        return {'scene': self.map_data['scene']}

    def handle_get_equipments_config(self, params: Dict) -> Dict:
        """处理获取装备配置的请求"""
        return {'equipments': self.configs['equipments']}

    def handle_get_buildings_config(self, params: Dict) -> Dict:
        """处理获取建筑配置的请求"""
        return {'buildings': self.configs['buildings']}

    def handle_npc_chat_update(self, params: Dict) -> Dict:
        """处理NPC聊天更新的请求"""
        return {'updated': True}