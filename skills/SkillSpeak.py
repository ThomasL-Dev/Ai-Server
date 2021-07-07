from binaries.obj.SkillObject import SkillObject
from binaries.obj.VoiceObject import VoiceObject
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillSpeak(SkillObject):

    utterance = ["dit"]

    cmd = "speak"

    need_param = True

    def on_execute(self):
        VoiceObject(self.__kernel__).speak(str(self.param))



