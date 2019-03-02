class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

        import os, sys
        python_path = os.path.join(self.behaviorAbsolutePath(), '/home/nao/.local/lib/python2.7/site-packages/')
        if python_path not in sys.path:
            sys.path.append(python_path)



    def client(self):
        import socket
        host = socket.gethostname()  # get local machine name
        port = 12336  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.connect(('193.205.116.65', port))

        message = input('-> ')
        while message != 'q':
            s.send(message.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            print('Received from server: ' + data)
            message = input('==> ')
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