from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvChannelDown(SkillObject):
    cmd = "tv_channeldown"

    utterance = ["chaine précédente"]

    need_param = True

    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.channel_down()




