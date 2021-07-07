from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvChannelUp(SkillObject):
    cmd = "tv_channelup"

    utterance = ["chaine suivante"]

    def on_execute(self):
        ip = self._kernel.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.channel_up()



