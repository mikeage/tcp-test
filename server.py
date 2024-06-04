# pylint: disable=missing-module-docstring,missing-function-docstring,line-too-long,too-many-nested-blocks
import logging
import select
import socket

# Define the server address and port
HOST = "0.0.0.0"
PORT = 12345

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
)
_LOGGER = logging.getLogger(__name__)


def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the server address and port
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    _LOGGER.info("Server listening on %s:%s", HOST, PORT)

    # List of sockets to monitor for incoming connections
    sockets_list = [server_socket]
    peer_info = {}

    try:
        while True:
            # Use select to get the list of sockets ready for reading
            read_sockets, _, exception_sockets = select.select(
                sockets_list, [], sockets_list
            )

            for notified_socket in read_sockets:
                # If the notified socket is the server socket, it means a new connection is coming in
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    peer_info[client_socket] = client_address
                    sockets_list.append(client_socket)
                    _LOGGER.info("%s\tAccepted new connection", client_address)

                # Otherwise, it's an existing connection sending data
                else:
                    try:
                        message = notified_socket.recv(4096)
                        if message:
                            _LOGGER.info(
                                "%s\tReceived message: %s",
                                notified_socket.getpeername(),
                                message.decode("utf-8"),
                            )
                        else:
                            # No message means the client has closed the connection
                            _LOGGER.warning(
                                "%s\tConnection closed",
                                peer_info.get(notified_socket, "Unknown"),
                            )
                            sockets_list.remove(notified_socket)
                            notified_socket.close()
                    except ConnectionResetError:
                        _LOGGER.warning(
                            "%s\tConnection reset",
                            peer_info.get(notified_socket, "Unknown"),
                        )
                        sockets_list.remove(notified_socket)
                        notified_socket.close()

            for notified_socket in exception_sockets:
                _LOGGER.warning(
                    "%s\tSocket exception",
                    peer_info.get(notified_socket, "Unknown"),
                )
                sockets_list.remove(notified_socket)
                del peer_info[notified_socket]
                notified_socket.close()

    except KeyboardInterrupt:
        _LOGGER.info("Server is shutting down...")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
