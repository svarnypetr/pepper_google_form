"""
Dummy client serves for testing
"""

import socket

PORT = 6558  # Make sure it's within the > 1024 $$ <65535 range


class Pepper(object):
    """
    Pepper replacement class
    """
    def __init__(self):
        self.position = -1
        self._input_list = []
        self.answer = ""

    def onInput_onString(self, _input_str):
        """
        We need to split the input string based on the percent separator
        '2%2%'.split('%') this split leads to the list ['2', '2', ''],
        therefore we remove the last member right-away by saying "all except the last one" -> [:-1]
        """
        processed_list = _input_str.split('%')[:-1]
        self._input_list = processed_list
        self.position = 0
        self.code()
        return

    def code(self):
        hello_statement = ''
        if self.position == 0:
            # I add the last value from the list but divide it by 100, it were %
            # I am using the format notation that is a little better and more versatile, read, google and learn
            hello_statement += "Hello {}.".format(self._input_list[self.position])
        #self.position = 1

        # while self.position < len(self._input_list):
        #     single_response = ''
        #     # we now iterate through the list with different behaviour for different parts of the list
        #     question_content = self._input_list[self.position]
        #     self.position += 1
        #     single_response += "Your vote is {}.".format(self._input_list[self.position])
        #     self.position += 1
        #     if self._input_list[self.position] == self._input_list[self.position - 1]:
        #         single_response += "That answer was correct."
        #     else:
        #         single_response += "That answer was not correct. The correct answer was: {}".format(
        #             self._input_list[self.position])
        #     self.position += 1
        #     question_number = (self.position - 1) / 3
        #     single_response = "The question {} was {}.".format(question_number, question_content) + single_response
        #     self.answer += single_response

        #self.answer = hello_statement + self.answer

        self.answer = hello_statement + "Your vote is: " + self._input_list[1] + "because: " + self._input_list[2]
        print(self.answer)


def client(stop=False):
    host = socket.gethostname()
    port = PORT

    s = socket.socket()
    s.connect((host, port))
    pepper = Pepper()

    received_message = False
    while not received_message:
        if stop:
            s.send('stop'.encode('utf-8'))
            s.close()
            break

        s.send('12345'.encode('utf-8'))
        received_message = s.recv(2048).decode('utf-8')
        # print('Received from server: ' + received_message)
        if received_message == 'matricola_error':
            print(received_message)
        else:
            pepper.onInput_onString(received_message)
        s.close()


if __name__ == '__main__':
    #client(True)
    client()
