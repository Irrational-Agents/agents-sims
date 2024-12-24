"""Main"""
import tornado.ioloop
import tornado.web
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    """
    WebSocket handler that echoes back any received messages.

    Methods
    -------
    open()
        Called when a new WebSocket connection is opened.
    on_message(message)
        Called when a message is received from the client.
    on_close()
        Called when the WebSocket connection is closed.
    """
    def open(self):
        """Called when a new WebSocket connection is opened."""
        print("WebSocket opened")

    def on_message(self, message):
        """
        Called when a message is received from the client.

        Parameters
        ----------
        message : str
            The message received from the client.
        """
        print(f"Received message: {message}")
        self.write_message(f"Echo: {message}")

    def on_close(self):
        """Called when the WebSocket connection is closed."""
        print("WebSocket closed")

def make_app():
    """
    Creates and returns a Tornado web application.

    Returns
    -------
    tornado.web.Application
        The Tornado web application configured with the WebSocket handler.
    """
    return tornado.web.Application([
        (r"/ws", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000,  address='0.0.0.0')
    print("WebSocket server is listening on ws://0.0.0.0:8000/ws")
    tornado.ioloop.IOLoop.current().start()
