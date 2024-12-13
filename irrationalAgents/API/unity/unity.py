# server.py
import socketio
import eventlet
from typing import Dict, Any
from datetime import datetime
from logger_config import setup_logger
from API.unity.handler import UnityHandlers

logger = setup_logger('API-unity')

class UnityServer:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        
        self.handlers = UnityHandlers()
        
        # 命令映射
        self.command_map = {
            'command.player.GetPlayerInfo': self.handlers.handle_get_player_info,
            'command.npc.GetNPCs': self.handlers.handle_get_npcs,
            'command.npc.GetNPCInfo': self.handlers.handle_get_npc_info,
            'command.map.NPCNavigate': self.handlers.handle_npc_navigate,
            'command.map.GetMapTown': self.handlers.handle_get_map_town,
            'command.map.GetMapScene': self.handlers.handle_get_map_scene,
            'command.config.GetEquipmentsConfig': self.handlers.handle_get_equipments_config,
            'command.config.GetBuildingsConfig': self.handlers.handle_get_buildings_config,
            'command.chat.NPCChatUpdate': self.handlers.handle_npc_chat_update
        }
        
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('command', self.handle_command)

    def on_connect(self, sid, environ):
        """处理客户端连接"""
        logger.info(f"Client connected: {sid}")

    def on_disconnect(self, sid):
        """处理客户端断开连接"""
        logger.info(f"Client disconnected: {sid}")

    def handle_command(self, sid: str, data: Dict[str, Any]):
        """处理所有客户端命令"""
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
            }, room=sid)
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            self.sio.emit('error', {
                'request_id': data.get('request_id'),
                'error': str(e)
            }, room=sid)

    def start(self, host: str = '0.0.0.0', port: int = 5001):
        """启动服务器"""
        logger.info(f"Starting unity server on {host}:{port}")
        eventlet.wsgi.server(eventlet.listen((host, port)), self.app)


if __name__ == '__main__':
    server = UnityServer()
    server.start()