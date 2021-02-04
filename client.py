"""
Dummy client serves for testing
"""

import socket

PORT = 6553  # Make sure it's within the > 1024 $$ <65535 range


class Pepper(object):
    """
    Pepper replacement class
    """
    def __init__(self):
        self.position = -1
        self._input_list = []
        self.answer = ""
        self.output_answer = ""

    def onInput_onString(self, _input_str):
        """
        We need to split the input string based on the percent separator
        '2%2%'.split('%') this split leads to the list ['2', '2', ''],
        therefore we remove the last member right-away by saying "all except the last one" -> [:-1]
        """
        processed_list = _input_str.split('%')[:-1]
        self._input_list = processed_list
        self.position = -1
        self.code()
        pass

    def onStopped(self):
        pass

    def code(self):
        if self.position == -1:
            # I add the last value from the list but divide it by 100, it were %
            # I am using the format notation that is a little better and more versatile, read, google and learn
            self.output_answer = "Ho ricevuto, {} risposte.".format(int(self._input_list[self.position])/100)
            self.position = 0

        while self.position < len(self._input_list)-2:
            # we now iterate through the list only until the before last member
            self.answer = "era {}.".format(self._input_list[self.position])
            self.position += 1
            self.answer = self.answer + "La risposta corretta e stata {} .".format(self._input_list[self.position])
            self.position += 1
            self.answer = self.answer + "e stata data la risposta esatta dal {} percent di voi.".format(self._input_list[self.position])
            self.position += 1
            self.output_answer += "La domanda " + str(self.position/3) + " " + self.answer

        if self.position == len(self._input_list)-2:
            self.answer = "In tutto le vostre risposte esatte sono state il {} percento.".format(self._input_list[self.position])
            self.onStopped()
            self.output_answer += "In tutto le vostre risposte esatte sono state il " + self.answer

        print(self.output_answer)


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
        s.send('give me data'.encode('utf-8'))
        received_message = s.recv(2048).decode('utf-8')
        print(received_message)
        pepper.onInput_onString(received_message)
        s.close()


if __name__ == '__main__':
    # client(True)
    client()
