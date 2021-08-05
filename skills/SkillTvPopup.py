from binaries.obj.SkillObject import SkillObject
from controllers.LgWebOsController import LgWebOsController
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillTvPopup(SkillObject):

    cmd = "tv_popup"

    utterance = ["popup sur la télé", "popup sur la télévision"]

    need_param = True

    def on_execute(self):
        ip = self.__kernel__.BootFile.get_value("lgwebos")
        controller = LgWebOsController(ip)
        controller.popup(self.param)

