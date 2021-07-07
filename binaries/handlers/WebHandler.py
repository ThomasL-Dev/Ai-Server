import tornado.web
import tornado.httpserver

# diasble tornado logs
import logging
hn = logging.NullHandler()
hn.setLevel(logging.NOTSET)
logging.getLogger("tornado.access").addHandler(hn)
logging.getLogger("tornado.access").propagate = False
# ===

from binaries.obj.AiObject import AiObject
from binaries.obj.HandlerObject import HandlerObject
from binaries.web.WebServer import WebServer

# ========================================== FIN DES IMPORTS ========================================================= #


class WebHandler(HandlerObject, AiObject):
    def __init__(self, kernel, port=8080):
        HandlerObject.__init__(self, kernel)

        # init web server port
        self.port = port

        # init web ip
        web_panel_ip = "{}:{}".format(self.__kernel__.server_private_ip, self.port)
        self.__console__.link("{} [IP] Address for Web Pannel : '{}'".format(self.__classname__, web_panel_ip), link=web_panel_ip)



    def on_handling(self):
        # init io loop
        self._ioloop = tornado.ioloop.IOLoop()
        # init the web server
        self._web_server = WebServer(self.__kernel__)
        # setting the web server to tornado loop
        self._http_server_api = tornado.httpserver.HTTPServer(self._web_server)
        # set listen port
        self.__set_listening_port()
        # start the ioloop and server
        self._ioloop.start()



    def __set_listening_port(self) -> None:
        # setting the listenning server port
        try:
            self._http_server_api.listen(self.port)
            self.__console__.info("{} Listening port set on '{}'".format(self.__classname__, self.port))
        except:
            self.__console__.error("{} Port '{}' already used".format(self.__classname__, self.port))
            # get a random port
            self.port = self.__get_random_port()
            self._http_server_api.listen(self.port)
            self.__console__.info("{} Listening port set on '{}'".format(self.__classname__, self.port))

    def __get_random_port(self) -> int:
        # return a random port when port already used
        # range between 10000 and 100000
        import random
        return int(random.randint(10000, 100000))

