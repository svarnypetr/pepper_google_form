import socket

## Dummy client serves for testing


def client():
    host = socket.gethostname()  # get local machine name
    port = 6553  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.connect((host, port))

    received_message = False
    while not received_message:
        s.send('give me data'.encode('utf-8'))
        received_message = s.recv(1024).decode('utf-8')
        print('Received from server: ' + received_message)
        s.send('stop'.encode('utf-8'))
    s.close()


if __name__ == '__main__':
    client()
