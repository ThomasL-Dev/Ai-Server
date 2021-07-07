from binaries.obj.SkillObject import SkillObject
from controllers.ComputerController import ComputerController
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillComputerPopup(SkillObject):

    utterance = ["popup sur pc", "popup sur ordi", "popup sur ordinateur"]

    cmd = "pc_popup"

    find_device_in_list = True

    need_param = True

    def on_execute(self):
        controller = ComputerController(self.ip)
        self.function = controller.popup(self.param)



