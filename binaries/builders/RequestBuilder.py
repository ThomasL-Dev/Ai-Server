import datetime
from binaries.obj.RequestObject import RequestObject
from binaries.obj.AiObject import AiObject

from controllers.TimeController import TimeController
from controllers.DateController import DateController
# ========================================== FIN DES IMPORTS ========================================================= #


class RequestBuilder(AiObject):

    def __init__(self, kernel, sender="None", user_input="None"):
        AiObject.__init__(self, kernel)

        # init request infos
        self._name = self.__generate_request_name()
        self._sender = sender
        self._input = user_input
        self._timestamp = str(self.__get_request_datetime())
        self._type = self.__get_input_type()

        # add request to list
        self.add_new_request(RequestObject(self.__kernel__, self._name, self._sender, self._input, self._timestamp, self._type))



    def add_new_request(self, request: RequestObject):
        # add request object to list
        self.__console__.info("{} Adding request '{}' to list".format(self.__classname__, self._name))
        self.__kernel__.RequestHandler.REQUESTS_LIST.append(request)



    def __generate_request_name(self):
        # generate a request name
        timestamp_req_name = str(self.__get_request_datetime()).replace(" ", "_").replace(":", "/").replace("/", "_")
        return str("request_" + timestamp_req_name)

    def __get_input_type(self):
        """ check si cest une commande ou non"""
        if self._input.split()[0].startswith("/"):
            return 'cmd'
        else:
            return 'text'

    def __get_request_datetime(self):
        # get timestamp request
        return TimeController.get_time() + " " + DateController.get_date()

