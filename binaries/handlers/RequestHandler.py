import time

from binaries.obj.AiObject import AiObject
from binaries.Logger import Logger
from binaries.obj.HandlerObject import HandlerObject
from binaries.processors.RequestProcessor import RequestProcessor
from binaries.obj.RequestObject import RequestObject

log = Logger()
# ========================================== FIN DES IMPORTS ========================================================= #




class RequestHandler(HandlerObject, AiObject):

    def __init__(self, kernel):
        HandlerObject.__init__(self, kernel)

        # init vars
        self._last_request = None

        # init request list
        self.REQUESTS_LIST = []



    def on_handling(self):
        """ handle check every second if new request """
        while True:
            # getting the lastet request
            request = self.__get_last_request_received()
            # if request is not None
            if request is not None:
                try:
                    self.__console__.info("{} New request '{}' received".format(self.__classname__, request.name))
                    self.__on_new_request(request)

                except Exception as e:
                    self.remove_request(request)
                    self.__console__.error('{} Error while on new request : {} '.format(self.__classname__, e))

            time.sleep(0.5)



    def remove_request(self, request: RequestObject) -> None:
        try:
            self.__console__.info("{} Removing request '{}'".format(self.__classname__, request.name))
            # itterate requests in list
            for request_in_list in self.REQUESTS_LIST:
                # if request object is the same as one in list
                if request.name == request_in_list.name:
                    # remove the request
                    self.REQUESTS_LIST.remove(request_in_list)
                    self.__console__.info("{} Request '{}' removed".format(self.__classname__, request.name))

        except Exception as e:
            self.__console__.error("{} Error while removing request '{}' : {} ".format(self.__classname__, request.name, e))



    def __on_new_request(self, request: RequestObject) -> None:
        # show request info in console
        self.__show_req_info(request)
        # send to discord
        self.__kernel__.DiscordHandler.send_log("Request {} '{}' received".format(request.name.capitalize(), request.input), self.__kernel__.BootFile.get_value("discord_channel_log_request"))
        # do the last request if asked
        if "encore" == request.input.lower():
            # then remove the 'again' request
            self.remove_request(request)
            # if the last request var is not None
            if self._last_request is not None:
                # set the new request to the lastest
                request = self._last_request
        # else do normal request
        else:
            # set last request used
            self._last_request = request
        # processing to request
        RequestProcessor(self.__kernel__, request=request).start()
        # remove request from list
        self.remove_request(request)

    def __get_last_request_received(self) -> RequestObject:
        try:
            # return the lastet request in list
            return self.REQUESTS_LIST[-1]
        except IndexError:
            # if there is no request return None
            return None

    def __show_req_info(self, request: RequestObject) -> None:
        # show the request info as a table in console
        title = "[RECEIVED] {}    ".format(request.name)
        t = self.__console__.table("\n" + title)
        t.add_column("Sender")
        t.add_column("Intent")
        t.add_column("Timestamp")
        t.add_column("Type")
        t.add_row(request.sender, request.input, request.timestamp, request.type)
        t.show()
