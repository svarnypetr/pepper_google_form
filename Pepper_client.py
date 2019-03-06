class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

        import os, sys
        python_path = os.path.join(self.behaviorAbsolutePath(), '/home/nao/.local/lib/python2.7/site-packages/')
        if python_path not in sys.path:
            sys.path.append(python_path)

    def client(self):
        import socket
        port = 12336  # Is this port the same as on your computer, i.e. the server?
        host_computer_IP = '193.205.116.65' # Is this the IP of your computer, i.e. the server?
        s = socket.socket()
        s.connect((host_computer_IP, port))
        received_message = False

        while not received_message:
            s.send('give form'.encode('utf-8'))
            received_message = s.recv(1024).decode('utf-8')
            self.Result(received_message)
        s.close()

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        #self.onStopped() #activate the output of the box
        self.client()

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box