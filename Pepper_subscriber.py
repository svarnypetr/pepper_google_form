class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        pass

    def onLoad(self):
        import threading
        self.lock = threading.RLock()
        self.signal = None
        self.linkId = -1

    def onUnload(self):
        with self.lock:
            self.unsubscribe()

    def onInput_onStart(self):
        with self.lock:
            self.unsubscribe()
            event = self.getParameter("event")

            if(len(event) == 0):
                self.onError("No event or signal given.")
                return

            params = event.split(".")
            if(len(params) == 2):
                try:
                    self.signal = getattr(self.session().service(params[0]), params[1])
                except Exception as e:
                    mem = self.session().service("ALMemory")
                    if(event in mem.getEventList()):
                        self.signal = mem.subscriber(event).signal
                    else:
                        self.onError(event + ": no such service.signal pair found, and no such event declared in ALMemory. Aborting.")
                        return
            else:
                self.signal = self.session().service("ALMemory").subscriber(event).signal

            self.linkId = self.signal.connect(self.reemitSignal)

    def onInput_onStop(self):
        with self.lock:
            self.unsubscribe()
            self.onStopped()

    def unsubscribe(self):
        if(self.signal is not None and self.linkId != -1):
            self.signal.disconnect(self.linkId)

        del self.signal
        self.signal = None
        self.linkId = -1

    def reemitSignal(self, *args):
        if(len(args) == 0):
            self.onEvent()
        elif(len(args) == 1):
            self.Result(args[0])
            self.onEvent(args[0])
        else:
            self.onEvent(args)