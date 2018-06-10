import pyttsx
import speech_recognition as sr

class Davos:

    def __init__(self,citidel):
        # self.__engine = pyttsx.init()
        # self.__r = sr.Recognizer()
        # self.__citidel=citidel
        pass

    def say_this(self,sentence):
        self.__engine.say(sentence)
        self.__engine.runAndWait()

    def listen_to_the_king(self):
        with sr.Microphone() as source:
            self.__r.adjust_for_ambient_noise(source, duration = 1)
            self.say_this(self.__citidel["davos_greet"])
            audio = self.__r.listen(source)
            t=self.__r.recognize_google(audio)
            return t
