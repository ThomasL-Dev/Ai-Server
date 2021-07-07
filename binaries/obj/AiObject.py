

class AiObject(object):

    def __init__(self, kernel):

        self.__classname__ = "[" + self.__class__.__name__ + "]"
        self.__kernel__ = kernel
        self.__console__ = kernel.console