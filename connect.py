import socket


class connection:
    def __init__(self, ip: str, port=10001):
        self.socket = socket.create_connection((ip, port))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.socket.close()

    def send(self, data):
        self.socket.sendall(data.encode('utf-8'))


if __name__ == '__main__':
    import datetime
    import time

    with connection('127.0.0.1') as conn:
        i = 10
        while i > 0:
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.send(cur_time)

            time.sleep(2)
            i -= 1
