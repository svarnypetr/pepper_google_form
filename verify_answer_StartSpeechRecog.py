import sys; sys.path.insert(0, "/home/nao/.local/lib/python2.7/site-packages/")
import speech_recognition as sr
#from gtts import gTTS  - Google text to speech
#import pygame

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self, p):
        # record italian or english speech
        speech = sr.AudioFile(p)
        rec = sr.Recognizer()
        with speech as source:
            audio = rec.record(source)
            try:
                recognized = rec.recognize_google(audio, language="it-IT")
                text=recognized.encode('utf-8').strip()
                self.logger.info(text)
                if text == 'yes':
                    self.output_onTranslated(text)
                else:
                    self.output_onFailedTranslation()
            except sr.RequestError:
                # API was unreachable or unresponsive
                self.logger.info("API unavailable")
                self.onFailedTranslation()
            except sr.UnknownValueError:
                # speech was unintelligible
                self.logger.info("Unable to recognize speech")
                self.onFailedTranslation()
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box