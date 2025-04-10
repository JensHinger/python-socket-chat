import socket
import threading

class Server():

    def __init__(self, address: tuple[str, int] = ("127.0.0.1", 56333)):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address

        self.connections = []

        try:
            self.start()

            while True:
                print("accepting new connections")
                conn, addr = self.server_socket.accept()

                self.connections.append((conn, addr))

                thread = threading.Thread(target=self.handle_user_connection, daemon=True, args=[conn, addr])
                thread.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            self.stop()

    def start(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen()
        print(f"Listening on {self.address}")

    def stop(self):
        self.server_socket.close()

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
                    print("ELSE BLOCK I GUESS")
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