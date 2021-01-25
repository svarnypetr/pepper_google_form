class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

        import os, sys
        python_path = os.path.join(self.behaviorAbsolutePath(), '/home/nao/.local/lib/python2.7/site-packages/')
        if python_path not in sys.path:
            sys.path.append(python_path)

    def client(self, name):
        import socket
        port = 6555  # Is this port the same as on your computer, i.e. the server?
        host_computer_IP = '192.168.0.101'  # Is this the IP of your computer, i.e. the server?
        s = socket.socket()
        s.connect((host_computer_IP, port))
        received_message = False

        while not received_message:
            s.send(name.encode('utf-8'))
            received_message = s.recv(2048).decode('utf-8')
            #self.logger.info(received_message)
            self.logger.info("Received message  " + str(received_message))
            if received_message == 'matricola_error':
                self.failed_matricola()
            else:
                self.Result(str(received_message))
            #s.send('stop'.encode('utf-8'))
        s.close()

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self, _input_str):
        #self.onStopped() #activate the output of the box
        self.client(_input_str)

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box