import socket
import threading

class Server():

    def __init__(self, address: tuple[str, int] = ("127.0.0.1", 56333)):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(5)
        self.address = address

        self.is_alive = True

        self.connection_thread = None
        self.connections = []

        try:
            self.start_server()
            self.connection_thread = threading.Thread(target=self.connect_new_user)
            self.connection_thread.start()
            
            print("Press any button to close")
            input("close:")
            raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("Manually shutting down server...")
        finally:
            self.is_alive = False
            self.stop_server()

    def start_server(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen()
        print(f"Listening on {self.address}")

    def stop_server(self):
        self.connection_thread.join()

        self.server_socket.close()
        print("Server closed")

    def connect_new_user(self):
        while self.is_alive:
            try:
                # .accept() throws error on timeout -> code below is not executed
                conn, addr = self.server_socket.accept()
            
                self.connections.append((conn, addr))

                thread = threading.Thread(target=self.handle_user_connection, daemon=True, args=[conn, addr])
                thread.start()
            except socket.timeout:
                continue

    def handle_user_connection(self, conn, addr):
        print(f"User connected: {addr}")
        try:
            while True:
                message = conn.recv(1024)
                print(f"{addr}: {message}")
                if message:
                    self.broadcast_message(message)
                    print("connections: ", self.connections)
                else:
                    # No data being sent -> close connection
                    conn.close()
                    break
        except ConnectionResetError as e:
            print(e)
        finally:
            print(f"closed connection to {addr}")
            self.connections.remove((conn, addr))

    def broadcast_message(self, message):
        for user in self.connections:
            user[0].send(message)
           

if __name__ == "__main__":
    s = Server()