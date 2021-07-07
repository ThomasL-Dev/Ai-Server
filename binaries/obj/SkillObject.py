from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #


class SkillObject(AiObject):

    utterance = []

    reponse = []

    ip = None

    param = None

    cmd = None

    need_param = False

    find_device_in_list = False



    def __init__(self, kernel):
        AiObject.__init__(self, kernel)

        # init private name
        self._name = f'{self.__class__.__name__}'



    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'ip={self.ip!r}, '
                f'param={self.param!r}, '
                f'cmd={self.cmd!r}, '
                f'need_param={self.need_param!r}, '
                f'find_device_in_list={self.find_device_in_list!r}, '
                f'utterance={self.utterance!r}'
                f')'
                )



    def on_execute(self):
        """ init controller """
        # controller = Controller() or if ip is not None Controller(ip)
        # self.function = controller.action()
        pass


    def exe(self) -> None:
        try:
            # execute the skill
            self.on_execute()

        except Exception as e:
            # raise error if failed
            raise Exception(str(e))
        # reset ip & param
        self.__reset_after_execute()



    def __reset_after_execute(self) -> None:
        # reset ip
        self.ip = None
        # reset param
        self.param = None
