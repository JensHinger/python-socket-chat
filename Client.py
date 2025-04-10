import socket
import threading

class Client():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_thread_lock = threading.Lock()

    def send_message(self):
        while True:
            with self.client_thread_lock:
                message = input("Type message: ")
            
            if message == "/c":
                self.socket.close()
                break

            self.socket.send(message.encode())
    
    def receive_message(self):
        try:
            while True:
                # Message should contain who sent it
                message = self.socket.recv(1024)
                print(f"\n{message.decode()}")
        finally:
            print("closed receive_message thread")
            
    def run(self):
        receive_message_thread = threading.Thread(target=self.receive_message, daemon=True)
        send_message_thread = threading.Thread(target=self.send_message)

        try:
            self.socket.connect(("127.0.0.1", 56333))
            receive_message_thread.start()
            send_message_thread.start()

            send_message_thread.join()

        finally:
            print("Chat closed.")
            self.socket.close()

if __name__ == "__main__":
    c = Client()
    c.run()