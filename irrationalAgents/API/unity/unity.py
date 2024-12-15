import socketio
import asyncio
import eventlet
from typing import Dict, Any
from logger_config import setup_logger
from API.unity.handler import UnityHandlers
from API.unity.request import UnityRequest
from API.unity.map_translator import MapTranslator

from datetime import datetime

logger = setup_logger('API-unity')
class UnityServer:
    def __init__(self):
        # Initialize socket.io server with CORS support
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        
        # State variables
        self.current_client_sid = None
        self.clock = 0
        self.initiated = False
        
        # Dependency initialization
        self.handlers = UnityHandlers()
        self.connected_event = eventlet.Event()
        self.map_translator = None
        
        # Command mappings
        self.command_map = {
            'command.player.GetPlayerInfo': 'handle_get_player_info',
            'command.npc.GetNPCs': 'handle_get_npcs',
            'command.npc.GetNPCInfo': 'handle_get_npc_info',
            'command.map.NPCNavigate': 'handle_npc_navigate',
            'command.map.GetMapTown': 'get_map_town',
            'command.map.GetMapScene': 'get_map_scene',
            'command.config.GetEquipmentsConfig': 'get_equipments_config',
            'command.config.GetBuildingsConfig': 'get_buildings_config',
            'command.chat.NPCChatUpdate': 'npc_chat_update',
            'ui.tick': self.update,
            'map.getTownData.response': 'handle_map_data',
            'map.getSceneMetadata.response': 'handle_meta_data',
            'config.getBlockData.response': 'handle_block_data'
        }
        
        # Register event handlers
        self.register_event_handlers()

    def register_event_handlers(self):
        """Register all socket.io event handlers."""
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        
        for command, handler_name in self.command_map.items():
            @self.sio.on(command)
            def event_handler(sid, data, command=command, handler_name=handler_name):
                handler = getattr(self.handlers, handler_name, None)
                if handler:
                    logger.info(f"Received command: {command}")
                    handler(data)
                else:
                    logger.info(f"No handler found for command: {command}")


    def on_connect(self, sid, environ):
        """Handle a new client connection."""
        self.current_client_sid = sid
        self.unity_request = UnityRequest(self.sio, self.current_client_sid)
        logger.info(f"Client connected: {sid}")
        if not self.connected_event.ready():
            self.connected_event.send(True)

    def on_disconnect(self, sid):
        """Handle client disconnection."""
        if sid == self.current_client_sid:
            self.current_client_sid = None
            self.unity_request = None
            logger.info(f"Client disconnected: {sid}")

    def wait_for_connection(self, timeout=60) -> bool:
        """Wait for a client connection within the specified timeout."""
        logger.debug(f"Waiting for client connection with timeout: {timeout}s")
        if self.connected_event.wait(timeout):
            logger.info("Client connected successfully.")
            return True
        logger.warning("Connection timeout exceeded.")
        return False

    def start_background(self):
        """Start the server in the background."""
        return eventlet.spawn(self.start)

    def init(self):
        """Perform server initialization tasks."""
        logger.info("Initializing server...")
        self.unity_request.get_map_meta_data()
        self.unity_request.get_map_data()
        self.unity_request.get_block_data()
        self.initiated = True

    def update(self, sid: str, data: Dict[str, Any]):
        """Handle updates from the client."""
        try:
            self.clock = int(data)
            if self.clock == 0:
                if not self.initiated:
                    self.init()
                if not self.handlers.map_data or not self.handlers.meta_data or not self.handlers.block_data:
                    self.unity_request.send_server_tick(0)
                else:
                    self.map_translator = MapTranslator(
                        self.handlers.map_data,
                        self.handlers.meta_data,
                        self.handlers.block_data
                    )
                    self.unity_request.send_server_tick(1)
            else:
                self.unity_request.send_server_tick(1)
        except ValueError as e:
            logger.error(f"Invalid data received for update: {data}. Error: {e}")

    def start(self, host: str = '0.0.0.0', port: int = 8080):
        """Start the Unity server."""
        logger.info(f"Starting Unity server on {host}:{port}")
        eventlet.wsgi.server(eventlet.listen((host, port)), self.app)

if __name__ == '__main__':
    server = UnityServer()
    server.start_background()

    logger.info("Waiting for client connection...")
    if server.wait_for_connection(timeout=30):  
        logger.info("Client connected, sending map request...")
        # server.unity_request.get_map_town()
        server.unity_request.get_buildings_config()
    else:
        logger.error("Timeout waiting for client connection.")
    
    try:
        while True:
            eventlet.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
