from typing import Dict, Callable, Optional
from datetime import datetime
from logger_config import setup_logger
import asyncio
import socketio

# Setup the logger for this module
logger = setup_logger('API-unity-request')

class UnityRequest:
    """
    A class to manage communication with a Unity client via Socket.IO.

    Attributes:
        sio: The Socket.IO server instance.
        current_client_sid: The session ID of the current client.
        _response_handlers: A dictionary mapping event names to their handlers.
    """

    def __init__(self, sio: socketio.AsyncServer, current_client_sid: str):
        """
        Initialize a UnityRequest instance.

        Args:
            sio: The Socket.IO server instance.
            current_client_sid: The session ID of the current client.
        """
        self.sio = sio
        self.current_client_sid = current_client_sid
        self._response_handlers: Dict[str, Callable[[Any], None]] = {}

    def emit(self, event_name: str, data: Optional[dict] = None) -> None:
        """
        Emit an event to the current client.

        Args:
            event_name: The name of the event to emit.
            data: Optional data to send with the event.
        """
        try:
            self.sio.emit(event_name, data, to=self.current_client_sid)
            logger.info(f"Emitted event '{event_name}' to client {self.current_client_sid}. Data: {data}")
        except Exception as e:
            logger.error(f"Error emitting event '{event_name}': {str(e)}")

    # def register_response_handler(self, event_name: str, handler: Callable[[Any], None]) -> None:
    #     """
    #     Register a response handler for a specific event.

    #     Args:
    #         event_name: The name of the event to handle.
    #         handler: The function to handle the event.
    #     """
    #     self._response_handlers[event_name] = handler
    #     logger.info(f"Registered handler for event '{event_name}'.")

    # def handle_response(self, event_name: str, data: Any) -> None:
        """
        Handle a response for a specific event.

        Args:
            event_name: The name of the event.
            data: The data associated with the event.
        """
        if event_name in self._response_handlers:
            try:
                self._response_handlers[event_name](data)
                logger.info(f"Handled response for event '{event_name}' from client {self.current_client_sid}.")
            except Exception as e:
                logger.error(f"Error handling response for event '{event_name}': {str(e)}")
        else:
            logger.warning(f"No handler registered for event '{event_name}'.")

    def send_server_tick(self, request_data: Optional[dict] = None) -> None:
        """Send Server tick for frame to be updated."""
        self.emit("server.tick", request_data)   

    def get_map_data(self, request_data: Optional[dict] = None) -> None:
        """Request town map data."""
        self.emit("map.getTownData", request_data)

    def get_map_meta_data(self, request_data: Optional[dict] = None) -> None:
        """Request map metadata."""
        self.emit("map.getSceneMetadata", request_data)

    def get_block_data(self, request_data: Optional[dict] = None) -> None:
        """Request building configuration data."""
        self.emit("config.getBlockData", request_data)

    def npc_chat_update(self, request_data: Optional[dict] = None) -> None:
        """Update NPC chat data."""
        self.emit("chat.updateNPC", request_data)
