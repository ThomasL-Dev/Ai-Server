import logging
_logger = logging.getLogger("comtypes")
_logger.setLevel(logging.CRITICAL)
import pyttsx3

from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #


class VoiceObject(AiObject):

    def __init__(self, kernel):
        AiObject.__init__(self, kernel)
        # init voice engine object
        self._engine = pyttsx3.init()
        # init voices
        self._voices = self._engine.getProperty('voices')
        # set the rate (voice speed)
        self._engine.setProperty('rate', 125)
        # set the voice
        self._engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\AI")



    def speak(self, reponse: str) -> None:
        try:
            self._engine.say(reponse)
            self._engine.runAndWait()
            self._engine.stop()

            self.__console__.info("{} {} says '{}'".format(self.__classname__, self.__kernel__.ia_name, reponse))

        except Exception as e:
            self.__console__.error("{} Error while speaking : {}".format(self.__classname__, e))


