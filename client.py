"""
Dummy client serves for testing
"""

import socket

PORT = 6555  # Make sure it's within the > 1024 $$ <65535 range


def pepper_processing(_input_str):
    _input_list = _input_str.split('%')[:-1]
    position = 0

    if position == 0:
        # I add the last value from the list but divide it by 100, it were %
        # I am using the format notation that is a little better and more versatile, read, google and learn
        print("Hello {}.".format(_input_list[position]))
        position = 1
    answer = ''
    while position < len(_input_list):
        # we now iterate through the list with different behaviour for different parts of the list
        answer += "The question was {}.".format(_input_list[position])
        position += 1
        answer += "Your answer was {}.".format(_input_list[position])
        position += 1
        if _input_list[position] == 1:
            answer += "That answer was correct."
        else:
            answer += "That answer was not correct. The correct answer was: {}".format(_input_list[position])
        position += 1

    print(answer)


def client():
    host = socket.gethostname()
    port = PORT

    s = socket.socket()
    s.connect((host, port))

    received_message = False
    while not received_message:
        s.send('81513'.encode('utf-8'))
        received_message = s.recv(1024).decode('utf-8')
        print('Received from server: ' + received_message)
        pepper_processing(received_message)
#       this allows to stop the server if needed
#        s.send('stop'.encode('utf-8'))
        s.close()


if __name__ == '__main__':
    client()
