import logging
import sys
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
        # plateform specific
        if "win32" in sys.platform:
            # set the rate (voice speed)
            self._engine.setProperty('rate', 125)
            # set the voice
            self._engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\AI")
        else:
            # set the rate (voice speed)
            self._engine.setProperty('rate', 110)
            # set the voice
            self._engine.setProperty("voice", self.__get_linux_voice_id())



    def speak(self, reponse: str) -> None:
        try:
            self._engine.say(reponse)
            self._engine.runAndWait()
            self._engine.stop()

            self.__console__.info("{} {} says '{}'".format(self.__classname__, self.__kernel__.ia_name, reponse))

        except Exception as e:
            self.__console__.error("{} Error while speaking : {}".format(self.__classname__, e))



    def __get_linux_voice_id(self):
        for voice in self._voices:
            if "french" == str(voice.id):
                return voice.id