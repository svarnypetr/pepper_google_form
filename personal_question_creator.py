class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.position = -1
        self._input_list = ""
        self.answer = ""


    def onLoad(self):
        #  put initialization code here
        self.position = -1
        self._input_list = []
        pass

    def onUnload(self):
        #  put clean-up code here
        self.position = "terminated"
        self._input_list = []
        pass

    def code(self):
        self.logger.info(self.position)

        if self.position == 0:
            # I add the last value from the list but divide it by 100, it were %
            # I am using the format notation that is a little better and more versatile, read, google and learn
            self.output_answer("Hello {}.".format(self._input_list[self.position]))
            self.position = 1

        while self.position < len(self._input_list):
        # we now iterate through the list with different behaviour for different parts of the list
            self.answer += "The question was {}.".format(self._input_list[self.position])
            self.position += 1
            self.answer += "Your answer was {}.".format(self._input_list[self.position])
            self.position += 1
            if self._input_list[self.position] == 1:
                self.answer += "That answer was correct."
            else:
                self.answer += "That answer was not correct. The correct answer was: {}".format(
                    self._input_list[self.position])
            self.position += 1
        self.output_answer(self.answer)

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
        pass

    def onInput_input(self):
        if not self.position == "terminated":
            self.code()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
