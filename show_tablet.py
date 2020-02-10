class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)


    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass


    def onInput_onStart(self, keyword):
        # show the new question
        self.showQuestion(keyword)
        self.output_matricola(keyword)
        # move
        self.onStopped()

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()


    def _getTabletService(self):
        tabletService = None
        try:
            tabletService = self.session().service("ALTabletService")
        except Exception as e:
            self.logger.error(e)
        return tabletService


    def _getMemoryService(self):
        service = None
        try:
            service = self.session().service("ALMemory")
        except Exception as e:
            self.logger.error(e)
        return service



    def showQuestion(self, p):
        self._getMemoryService().insertData('keyword', p)
        tabService = self._getTabletService()
        ip = tabService.robotIp()
        uid = self.packageUid()
        url = 'http://' + ip + '/apps/' + uid + '/index.html'
        tabService.loadUrl(url)
        tabService.showWebview()


    def hideQuestion(self):
        tabService = self._getTabletService()
        tabService.hideWebview()