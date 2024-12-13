from typing import Dict, Any
from datetime import datetime
from logger_config import setup_logger
import asyncio

logger = setup_logger('API-unity-request')

class UnityRequest():
    def __init__(self, sio, current_client_sid):
       self.sio = sio
       self.current_client_sid = current_client_sid

    async def get_map_town(self, params: Dict = None) -> Dict:
        try:
            response_future = asyncio.Future()

            def on_response(data):
                if not response_future.done():
                    response_future.set_result(data)

            self.sio.on('command.map.GetMapTown', on_response)

            self.sio.emit(
                'command.map.GetMapTown', 
                params or {}, 
                room=self.current_client_sid
            )

            response = await asyncio.wait_for(response_future, timeout=10)
            
            return {'success': True, 'data': response}

        except asyncio.TimeoutError:
            return {'error': 'Timeout waiting for map town response'}
        except Exception as e:
            logger.error(f"Error requesting map town: {str(e)}")
            return {'error': str(e)}