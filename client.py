"""
Dummy client serves for testing
"""

import socket

PORT = 6557  # Make sure it's within the > 1024 $$ <65535 range


def pepper_processing(_input_str):
    _input_list = _input_str.split('%')[:-1]
    position = 0

    hello_statement = ''
    if position == 0:
        # I add the last value from the list but divide it by 100, it were %
        # I am using the format notation that is a little better and more versatile, read, google and learn
        hello_statement += "Hello {}.".format(_input_list[position])
        position = 1
    answer = ''
    while position < len(_input_list):
        single_response = ''
        # we now iterate through the list with different behaviour for different parts of the list
        question_content = _input_list[position]
        position += 1
        single_response += "Your answer was {}.".format(_input_list[position])
        position += 1
        if _input_list[position] == 1:
            single_response += "That answer was correct."
        else:
            single_response += "That answer was not correct. The correct answer was: {}".format(_input_list[position])
        position += 1
        question_number = (position-1)/3
        single_response = "The question {} was {}.".format(question_number, question_content) + single_response
        answer += single_response

    answer = hello_statement + answer
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
        # print('Received from server: ' + received_message)
        if received_message == 'matricola_error':
            print(received_message)
        else:
            pepper_processing(received_message)
#       this allows to stop the server if needed
#        s.send('stop'.encode('utf-8'))
        s.close()


if __name__ == '__main__':
    client()
