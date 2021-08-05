from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillTvLaunchApp(SkillObject):

    cmd = "tv_launch"

    utterance = ["lance sur la télé", "lance sur la télévision"]

    need_param = True

    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.launch_app(self.param)

