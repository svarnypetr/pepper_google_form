class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)


    def onLoad(self):
        #put initialization code here
        self.position = 0
        self._input_str = ""
        pass

    def onUnload(self):
        #put clean-up code here
        self.position = 0
        self._input_str = ""
        pass

    def code(self):
        if self.position < len(self._input_str)-1:
            self.counts(str(self._input_str[self.position]))
            self.position += 1
            self.question_count("Question " + str(self.position))
        elif  self.position == len(self._input_str)-1:
            self.onStopped(str(self._input_str[self.position]))
            self.question_count("Overall ")
        else:
            pass


    def onInput_onString(self, _input_str):
        self._input_str = _input_str
        self.code()
        pass

    def onInput_input(self):
        self.code()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
