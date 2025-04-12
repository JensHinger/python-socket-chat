import socket
import threading

class Client():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_thread_lock = threading.Lock()

        self.run()

    def send_message(self):
        try:
            while True:
                message = input("Type message: ")
                
                if message == "/c":
                    self.socket.close()
                    break

                self.socket.send(message.encode())
        except ConnectionResetError as e:
            print(e)
    
    def receive_message(self):
        try:
            while True:
                message = self.socket.recv(1024)
                if message:
                    print(f"{message.decode()} \n")
        except ConnectionResetError as e:
            print(e)
        finally:
            print("closed receive_message thread")
            
    def run(self):
        receive_message_thread = threading.Thread(target=self.receive_message)
        send_message_thread = threading.Thread(target=self.send_message, daemon=True)

        try:
            self.socket.connect(("127.0.0.1", 56333))
            receive_message_thread.start()
            send_message_thread.start()

            receive_message_thread.join()

        finally:
            print("Chat closed.")
            self.socket.close()

if __name__ == "__main__":
    c = Client()