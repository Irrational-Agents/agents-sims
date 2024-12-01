import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from models import NPCModel
from logger_config import setup_logger
from irrationalAgents.agent import gen_agent_by_name
from irrationalAgents.agents_modules.behavior.action import handle_chat

logger = setup_logger('API-server-handler')

NPC_STORAGE_BASE_PATH = "storage/sample_data/agents"

def ensure_npc_dir_exists(npc_name: str):
    """Ensure directory for specific NPC exists"""
    npc_dir = os.path.join(NPC_STORAGE_BASE_PATH, npc_name)
    os.makedirs(npc_dir, exist_ok=True)
    return npc_dir

def get_npc_file_path(npc_name: str):
    return os.path.join(NPC_STORAGE_BASE_PATH, npc_name, "data.json")

def load_npc(npc_name: str) -> NPCModel:
    try:
        file_path = get_npc_file_path(npc_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            npc_data = json.load(f)
            logger.info(f"Successfully loaded NPC: {npc_name}")
            return NPCModel(**npc_data)
    except FileNotFoundError:
        logger.warning(f"NPC data not found: {npc_name}")
        raise HTTPException(status_code=404, detail=f"NPC '{npc_name}' not found")
    except json.JSONDecodeError:
        logger.error(f"Error parsing NPC data: {npc_name}")
        raise HTTPException(status_code=500, detail=f"Error parsing NPC data for '{npc_name}'")

def save_npc(npc: NPCModel):
    """Save NPC data to JSON file"""
    try:
        ensure_npc_dir_exists(npc.name)
        
        file_path = get_npc_file_path(npc.name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(npc.model_dump(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"Successfully saved NPC data: {npc.name}")
    except Exception as e:
        logger.error(f"Error saving NPC data: {npc.name}, {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving NPC data for '{npc.name}'")

def list_npcs() -> List[str]:
    try:
        os.makedirs(NPC_STORAGE_BASE_PATH, exist_ok=True)
        
        # List all
        npcs = [
            name for name in os.listdir(NPC_STORAGE_BASE_PATH) 
            if os.path.isdir(os.path.join(NPC_STORAGE_BASE_PATH, name))
        ]
        
        logger.info(f"Listed {len(npcs)} NPCs")
        return npcs
    except Exception as e:
        logger.error(f"Error listing NPCs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listing NPCs")
