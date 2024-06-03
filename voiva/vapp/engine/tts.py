''' translates test to speech '''

import pyttsx3

class VoivaTTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def vtts(self, text):
        if text:
            self.engine.say(text)
            self.engine.runAndWait()
            return "Text translated to speech successfully!"
        else:
            return "Please enter some text before translating."
