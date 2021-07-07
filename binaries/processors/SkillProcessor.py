from binaries.obj.SkillObject import SkillObject
from binaries.builders.ReponseBuilder import ReponseBuilder
from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillProcessor(AiObject):

    def __init__(self, kernel, skill: SkillObject, sender):
        AiObject.__init__(self, kernel)

        # init sender
        self.sender = sender
        # skill infos
        self.skill = skill
        self.skill_name = skill._name


    def process(self, ip: str=None, param: str=None) -> None:
        self.__console__.info("{} Processing Skill '{}'".format(self.__classname__, self.skill_name))
        # checking ip
        self.__check_ip(ip)
        # checkin param
        self.__check_param(param)

        try:
            # execute the skill
            self.skill.exe()
            # build a reponse
            ReponseBuilder(self.__kernel__, self.sender, self.skill.reponse)
            # showing execute infos
            if ip is None and param is None:
                self.__console__.info("{} Skill '{}' processed".format(self.__classname__, self.skill_name), color="green")

            elif ip is not None and param is not None:
                self.__console__.info("{} Skill '{}' processed with ip '{}' & param '{}'".format(self.__classname__, self.skill_name, ip, param), color="green")

            elif ip is not None:
                self.__console__.info("{} Skill '{}' processed with ip '{}'".format(self.__classname__, self.skill_name, ip), color="green")

            elif param is not None:
                self.__console__.info("{} Skill '{}' processed with param '{}'".format(self.__classname__, self.skill_name, param), color="green")

        except Exception as e:
            ReponseBuilder(self.__kernel__, self.sender, "Impossible d'éxécuté cette action")
            self.__console__.error("{} Error while executing Skill '{}' : {}".format(self.__classname__, self.skill_name, e))


    def __check_param(self, param: str) -> None:
        # if param is not None
        if param is not None:
            # setting param
            self.skill.param = param
        else:  # if is not and need param raise error
            if self.skill.need_param:
                raise Exception("{} Need a param to execute '{}'".format(self.__classname__, self.skill_name))


    def __check_ip(self, ip: str) -> None:
        # if ip is not None
        if ip is not None:
            # setting ip
            self.skill.ip = ip
        else:   # if is not and need ip raise error
            if self.skill.find_device_in_list:
                raise Exception("{} Need an ip to execute '{}'".format(self.__classname__, self.skill_name))

