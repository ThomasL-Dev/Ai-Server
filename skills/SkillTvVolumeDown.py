from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvVolumeDown(SkillObject):
    cmd = "tv_volumedown"

    utterance = ["baisse le son de la télé", "baisse le son de la télévision", "baisse le volume de la télé", "baisse le volume de la télévision"]

    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.volume_down()



