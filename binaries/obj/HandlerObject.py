from threading import Thread
from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #


class HandlerObject(Thread, AiObject):

    def __init__(self, kernel):
        Thread.__init__(self)
        AiObject.__init__(self, kernel)

        self.setDaemon(True)

        self.__console__.info("{} Initializing ...".format(self.__classname__))


    def on_handling(self):
        pass

    def run(self):
        try:
            self.__console__.kernel("{} Started".format(self.__classname__))
            self.on_handling()
        except Exception as e:
            self.__console__.error("{} Failed to start : {}".format(self.__classname__, e))
