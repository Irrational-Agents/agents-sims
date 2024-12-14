# server.py
import socketio
import asyncio
import eventlet
from typing import Dict, Any
from datetime import datetime
from logger_config import setup_logger
from API.unity.handler import UnityHandlers
from API.unity.request import UnityRequest

logger = setup_logger('API-unity')

class UnityServer:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.current_client_sid = None
        
        self.handlers = UnityHandlers()
        self.connected_event = eventlet.Event()
        
        # 命令映射
        self.command_map = {
            'command.player.GetPlayerInfo': self.handlers.handle_get_player_info,
            'command.npc.GetNPCs': self.handlers.handle_get_npcs,
            'command.npc.GetNPCInfo': self.handlers.handle_get_npc_info,
            'command.map.NPCNavigate': self.handlers.handle_npc_navigate,
            'command.map.GetMapTown': self.handlers.get_map_town,
            # 'command.map.GetMapScene': self.handlers.get_map_scene,
            # 'command.config.GetEquipmentsConfig': self.handlers.get_equipments_config,
            # 'command.config.GetBuildingsConfig': self.handlers.get_buildings_config,
            # 'command.chat.NPCChatUpdate': self.handlers.npc_chat_update
        }
        
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)

        # I am sending data on same Channel name so this will not work
       # self.sio.on('command', self.handle_command)

        self.sio.on('command.map.GetMapTown', self.handlers.get_map_town)
        self.sio.on('tick', self.handlers.handle_tick)

    def on_connect(self, sid, environ):
        self.current_client_sid = sid
        self.unity_request = UnityRequest(server.sio, server.current_client_sid)
        logger.info(f"Client connected: {sid}")
        if not self.connected_event.ready():
            self.connected_event.send(True)

        # adding sio for tick
        self.handlers.sio = self.sio


    def on_disconnect(self, sid):
        self.current_client_sid = None
        self.unity_request = None
        logger.debug(f"Client disconnected: {sid}")
    
    def wait_for_connection(self, timeout=60):
        logger.debug(f"Starting wait_for_connection with timeout: {timeout}")
        logger.debug(f"Current event state: {self.connected_event.ready()}")
        success = self.connected_event.wait(timeout)
        logger.info(f"Wait completed, success: {success}")
        if success:
            logger.debug("Connection confirmed")
            return True
        return False
    
    def start_background(self):
        return eventlet.spawn(self.start)

    def handle_command(self, sid: str, data: Dict[str, Any]):
        try:
            command = data.get('command')
            params = data.get('parameters', {})
            request_id = data.get('request_id')
            
            logger.info(f"Received command: {command} from {sid}")
            
            handler = self.command_map.get(command)
            if not handler:
                raise ValueError(f"Unknown command: {command}")
                
            response = handler(params)
            
            self.sio.emit('response', {
                'request_id': request_id,
                'data': response,
                'timestamp': datetime.now().isoformat()
            }, to=sid)
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            self.sio.emit('error', {
                'request_id': data.get('request_id'),
                'error': str(e)
            }, room=sid)

    def start(self, host: str = '0.0.0.0', port: int = 8080):
        logger.info(f"Starting unity server on {host}:{port}")
        eventlet.wsgi.server(eventlet.listen((host, port)), self.app)


if __name__ == '__main__':
    server = UnityServer()
    server.start_background()

    logger.debug("Waiting for client connection...")
    if server.wait_for_connection(timeout=30):  
        logger.info("Client connected, sending map request...")
        server.unity_request.get_map_town()
    else:
        logger.error("Timeout waiting for client connection")
    
    try:
        while True:
            eventlet.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")