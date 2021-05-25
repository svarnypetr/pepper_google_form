# Pepper Python module content 

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.matricola = ''

    def onLoad(self):
        self.ok = [False]*2

    def onUnload(self):
        #puts code for box cleanup here
        ""

    def onStart(self, nInput):
        self.ok[nInput-1] = True
        bOutput = True
        for bOk in self.ok:
            bOutput = bOutput and bOk
        if( bOutput ):
            self.ok = [False]*2
            self.signalsReceived()
            self.output(self.matricola)

    def onInput_signal1(self):
        self.onStart(1)

    def onInput_signal2(self):
        self.onStart(2)

    def onInput_input(self, _input_str):
        self.matricola = _input_str
