class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.position = -1
        self._input_list = ""
        self.answer = ""


    def onLoad(self):
        #put initialization code here
        self.position = -1
        self._input_list = []
        pass

    def onUnload(self):
        #put clean-up code here
        self.position = "terminated"
        self._input_list = []
        pass


    def code(self):
        self.logger.info(self.position)

        if self.position == -1:
            # I add the last value from the list but divide it by 100, it were %
            # I am using the format notation that is a little better and more versatile, read, google and learn
            self.output_answer("Questions were answered by {} students".format(int(self._input_list[self.position])/100))
            self.position = 0

        # we now iterate through the list only until the before last member
        elif self.position < len(self._input_list)-2:
            self.answer = "was {}.".format(self._input_list[self.position])
            self.position += 1
            self.answer = self.answer + "The correct answer was {} .".format(self._input_list[self.position])
            self.position += 1
            self.answer = self.answer + "It was answered correctly by {} percent.".format(self._input_list[self.position])
            self.position += 1
            self.output_answer("Question " + str(self.position/3) + " " + self.answer)

        elif self.position == len(self._input_list)-2:
            self.answer = "the answers were on {} percent correct.".format(self._input_list[self.position])
            self.onStopped()
            self.output_answer("Overall " + self.answer)

        else:
            pass


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

    def onInput_input(self):
        if not self.position == "terminated":
            self.code()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
