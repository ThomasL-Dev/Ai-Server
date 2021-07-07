from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillTvVolumeUp(SkillObject):
    cmd = "tv_volumeup"

    utterance = ["monte le son de la télé", "monte le son de la télévision", "monte le volume de la télé", "monte le volume de la télévision"]

    def on_execute(self):
        ip = self._kernel.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.volume_up()




