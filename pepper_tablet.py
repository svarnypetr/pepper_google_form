# Pepper Python module content 

import re

class MyClass(GeneratedClass):

    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        self.isRunning = False

    def onUnload(self):
        self.isRunning = False

    def _getTabletService(self):
        tabletService = None
        try:
            tabletService = self.session().service("ALTabletService")
        except Exception as e:
            self.logger.error(e)
        return tabletService

    def onInput_onStart(self):
        if self.isRunning:
            return  # already running, nothing to do
        self.isRunning = True
        # We create TabletService here in order to avoid
        # problems with connections and disconnections of the tablet during the life of the application
        tabletService = self._getTabletService()
        appName = self.packageUid()
        if appName:
            if tabletService:
                if tabletService.loadApplication(appName):
                    tabletService.showInputTextDialog("Example dialog", "OK", "Cancel")
                    signal_id = 0
                    self.logger.info("Successfully set application: %s" % appName)
                    tabletService.showWebview()

                    def is_matricola():
                        matricola_pattern = r"^[0-9]{5}"
                        return re.findall(matricola_pattern, client_data)

                    def callback(button_id, input_text):
                        if button_id == 1:
                            self.logger.info("input_text: %s" % input_text)
                            if is_matricola():
                                self.onSuccess(input_text)
                            else:
                                self.onFailure()
                                self.logger.info("wrong matricola")
                        if button_id == 0:
                            self.onFailure()
                            self.logger.info("cancel pressed")
                        tabletService.onInputText.disconnect(signal_id)
                        self.isRunning = False

                    signal_id = tabletService.onInputText.connect(callback)

                else:
                    self.logger.warning("Got tablet service, but failed to set application: %s" % appName)
            else:
                self.logger.warning("Couldn't find tablet service, so can't set application: %s" % appName)
