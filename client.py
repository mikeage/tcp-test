# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long,too-many-nested-blocks
import signal
import sys
import socket
import time
import os
import logging

# Define the server address and port to connect to
SOURCE_PORT = int(os.getenv("SOURCE_PORT", "0"))
TARGET_HOST = os.getenv("HOST", "127.0.0.1")
TARGET_PORT = int(os.getenv("PORT", "12345"))
POD_NAME = os.getenv("POD_NAME", "n/a")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
)
_LOGGER = logging.getLogger(__name__)


def handle_sigterm(__signum__, __frame__):
    _LOGGER.warning("Received SIGTERM")
    sys.exit(0)


signal.signal(signal.SIGTERM, handle_sigterm)


def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.bind(("", SOURCE_PORT))
        client_socket.connect((TARGET_HOST, TARGET_PORT))
        host, port = client_socket.getpeername()

        _LOGGER.info(
            "%s:%s\tconnected (to %s:%s)", host, port, TARGET_HOST, TARGET_PORT
        )
        counter = 0

        client_socket.sendall(f"name:{POD_NAME}".encode())
        while True:
            time.sleep(1)

            try:
                client_socket.sendall(f"ctr:{counter} from {POD_NAME}".encode())
                _LOGGER.info("%s:%s\tSent %d", host, port, counter)
                counter += 1

            except (BrokenPipeError, ConnectionResetError) as e:
                _LOGGER.warning("%s:%s\tConnection error: %s", host, port, e)
                break
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.error("%s:%s\tUnexpected error: %s", host, port, e)
                break

    except ConnectionRefusedError:
        _LOGGER.info("%s:%s\tConnection refused", TARGET_HOST, TARGET_PORT)

    finally:
        client_socket.close()
        _LOGGER.warning("Connection closed")


if __name__ == "__main__":
    main()
