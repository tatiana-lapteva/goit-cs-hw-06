
import asyncio
import socket
import websockets
import logging
from datetime import datetime
from mongo_handler import save_message
import json


# Constants
WEBSOCKET_PORT = 5000


async def handler(websocket, path):
    """Receives and processes websocket messages."""
    logging.info("Client connected")
    try:
        data = await websocket.recv()
        logging.info(f"Received raw data: {data}")
        message_data = data.decode('utf-8')
        logging.info(f"Decoded data: {message_data}")
        username, message = message_data.split(': ')
        data = {
            "date": datetime.now(),
            "username": username,
            "message": message
        }
        response = await save_message(data)
        await websocket.send(response)
    except websockets.exceptions.ConnectionClosedOK:
        logging.info("Client closed connection normally")
    except json.JSONDecodeError:
        error_msg = "Invalid JSON received"
        logging.error(error_msg)
        await websocket.send(json.dumps({"status": "error", "message": error_msg}))
    except Exception as e:
        logging.error(f"Unexpected error in WebSocket handler: {e}")
        await websocket.send(json.dumps({"status": "error", "message": str(e)}))
    finally:
        await websocket.close()


async def start_websocket_server():
    """Starts the WebSocket server and listens for incoming connections."""
    try:
        async with websockets.serve(handler, "0.0.0.0", WEBSOCKET_PORT, reuse_address=True):
            logging.info(f"WebSocket server is running on ws://localhost:{WEBSOCKET_PORT}")
            await asyncio.Future()

    except Exception as e:
        logging.error(f"Error starting WebSocket server: {e}")


def run_websocket_server():
    """Runs the WebSocket server in a new process."""
    asyncio.run(start_websocket_server())
