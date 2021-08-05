from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvShutdown(SkillObject):
    cmd = "tv_shutdown"

    utterance = ["éteint la télé", "éteint la télévision"]

    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.shutdown()



