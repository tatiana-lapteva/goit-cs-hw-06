
import threading
import logging
from http_server import run_http_server

from websocket_server import run_websocket_server


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    
    http_thread = threading.Thread(target=run_http_server)
    websocket_thread = threading.Thread(target=run_websocket_server)

    http_thread.start()
    websocket_thread.start()

    http_thread.join()
    websocket_thread.join()
