import socket
import time

# Define the server address and port to connect to
HOST = '127.0.0.1'  # Change to the server's IP address if it's remote
PORT = 12345

def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')
        
        while True:
            try:
                # Send one byte of data
                client_socket.sendall(b'\x01')
                print('Sent one byte to the server')
                
                # Wait for one second before sending the next byte
                time.sleep(1)
            
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f'Connection error: {e}')
                break
    
    except ConnectionRefusedError:
        print(f'Failed to connect to {HOST}:{PORT}')
    
    finally:
        client_socket.close()
        print('Connection closed')

if __name__ == "__main__":
    main()

