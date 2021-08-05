from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvConnect(SkillObject):

    cmd = "tv_connect"

    utterance = ["connecte à la télé", "connecte à la télévision"]



    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller._connect_tv()




