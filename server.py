import socket
import select
import sys

# Define the server address and port
HOST = '0.0.0.0'
PORT = 12345

def log_message(message):
    print(message)

def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the server address and port
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    log_message(f'Server listening on {HOST}:{PORT}')
    
    # List of sockets to monitor for incoming connections
    sockets_list = [server_socket]
    
    try:
        while True:
            # Use select to get the list of sockets ready for reading
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            
            for notified_socket in read_sockets:
                # If the notified socket is the server socket, it means a new connection is coming in
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets_list.append(client_socket)
                    log_message(f'Accepted new connection from {client_address}')
                
                # Otherwise, it's an existing connection sending data
                else:
                    try:
                        message = notified_socket.recv(4096)
                        if message:
                            log_message(f'Received message from {notified_socket.getpeername()}: {message.decode("utf-8")}')
                        else:
                            # No message means the client has closed the connection
                            log_message(f'Connection closed by {notified_socket.getpeername()}')
                            sockets_list.remove(notified_socket)
                            notified_socket.close()
                    except ConnectionResetError:
                        log_message(f'Connection reset by peer {notified_socket.getpeername()}')
                        sockets_list.remove(notified_socket)
                        notified_socket.close()
            
            for notified_socket in exception_sockets:
                log_message(f'Socket exception on {notified_socket.getpeername()}')
                sockets_list.remove(notified_socket)
                notified_socket.close()
    
    except KeyboardInterrupt:
        log_message('Server is shutting down...')
    
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()

