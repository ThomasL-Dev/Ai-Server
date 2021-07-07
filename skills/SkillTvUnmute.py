from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillTvUnmute(SkillObject):

    cmd = "tv_unmute"

    utterance = ["mute la télé", "mute la télévision"]

    def on_execute(self):
        ip = self._kernel.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.unmute()

