import sys
import socket


class Client:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def start(self):
        for idx in range(2):
            s = self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(self.socket_path)
            message = "東京 天気"
            sys.stdout.write("send to server ({}): {}\n".format(idx, message))
            s.send(message.encode())
            data = s.recv(1024)
            sys.stdout.write("receive from server: {}\n".format(data.decode()))
            s.close()


def main():
    client = Client('/tmp/org.freasearch.intelligence-engine/weather.sock')
    client.start()

if __name__ == '__main__':
    main()
