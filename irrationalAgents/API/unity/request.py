from typing import Dict, Any
from datetime import datetime
from logger_config import setup_logger
import asyncio
import socketio

logger = setup_logger('API-unity-request')
class UnityRequest:
    def __init__(self, sio, current_client_sid):
        self.sio = sio
        self.current_client_sid = current_client_sid
        self._response_handlers = {}
        
    def emit(self, event_name, data=None):
        try:
            self.sio.emit(event_name, data, to=self.current_client_sid)
            logger.info(f"Emitted {event_name} to client {self.current_client_sid}")
        except Exception as e:
            logger.error(f"Error emitting {event_name}: {str(e)}")

    def register_response_handler(self, event_name, handler):
        self._response_handlers[event_name] = handler
        
    def handle_response(self, event_name, data):
        # should be used for response but since all the command named as command.
        # so this one is replaced in unity.py
        if event_name in self._response_handlers:
            try:
                self._response_handlers[event_name](data)
                logger.info(f"Handled response for {event_name} from client {self.current_client_sid}")
            except Exception as e:
                logger.error(f"Error handling response for {event_name}: {str(e)}")
        else:
            logger.warning(f"No handler registered for event: {event_name}")
            
    def get_map_town(self, request_data=None):
        self.emit("command.map.GetMapTown", request_data)

    def get_map_scene(self, request_data=None):
        self.emit("command.map.GetMapScene", request_data)
    
    def get_equipments_config(self, request_data=None):
        self.emit("command.config.GetEquipmentsConfig", request_data)

    def get_buildings_config(self, request_data=None):
        self.emit("command.config.GetBuildingsConfig", request_data)
    
    def npc_chat_update(self, request_data=None):
        self.emit("command.chat.NPCChatUpdate", request_data)
        
    def send_message(self, message):
        self.emit("message", message)
