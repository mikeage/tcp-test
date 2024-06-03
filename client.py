# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long,too-many-nested-blocks
import socket
import time
import os
import logging

# Define the server address and port to connect to
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "12345"))

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        _LOGGER.info("Connected to %s:%s", HOST, PORT)
        counter = 0

        while True:
            try:
                client_socket.sendall(str(counter).encode())
                _LOGGER.info("Sent %d to the server", counter)
                counter += 1

                # Wait for one second before sending the next byte
                time.sleep(1)

            except (BrokenPipeError, ConnectionResetError) as e:
                _LOGGER.warning("Connection error: %s", e)
                break

    except ConnectionRefusedError:
        _LOGGER.info("Failed to connect to %s:%s", HOST, PORT)

    finally:
        client_socket.close()
        _LOGGER.warning("Connection closed")


if __name__ == "__main__":
    main()
