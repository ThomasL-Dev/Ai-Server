import os
import sys
import inspect
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
from binaries.web.obj.Error404Handler import Error404Handler
# ========================================== FIN DES IMPORTS ========================================================= #


class WebServer(tornado.web.Application, AiObject):

    def __init__(self, kernel):
        AiObject.__init__(self, kernel)
        # init routes path
        self._routes_path = os.path.join(os.getcwd(), "binaries", "web", "routes")
        # init static folders
        self._templates_path = os.path.join(os.getcwd(), "binaries", "web", "templates")
        self._static_path = os.path.join(os.getcwd(), "binaries", "web", "static")
        # init cameras feed path
        self._cameras_path = os.path.join(os.getcwd(), "cameras")
        # init params dict for web pages
        self._params_dict = {"kernel": self.__kernel__}
        # init routes list
        self.ROUTES = []
        # loading every routes in folder
        self.__load_routes(self._routes_path)
        # make setting for tornado server
        settings = {
            "template_path": self._templates_path,
            "static_path": self._static_path,
            "cameras_path": self._cameras_path,
            "default_handler_class": Error404Handler,
            "cookie_secret": "web_io_token",
        }
        tornado.web.Application.__init__(self, self.ROUTES, **settings)


    def __load_routes(self, path: str):
        """Get a list of files in the directory, if the directory exists"""
        # itterate (folder path, folder name, files) in folder and sub folder
        for (dirpath, dirnames, filenames) in os.walk(path):
            # ittterate foute file in folder
            for route_file_name in self.__found_route_in_folder(dirpath):
                # load route class in file
                route_class = self.__load_route_class_by_file_name(route_file_name)
                # route file path
                route_file_path = os.path.join(dirpath, route_file_name)
                # create the route
                route = self.__create_route(route_file_path.replace("\\", "/"))  # .replace() avoid error path on windows
                # if route class is not None
                if route_class is not None:
                    # if route not already exist
                    if not self.__if_route_exist_in_list(route):
                        # check the route name if is specific
                        route = self.__check_route_name(route)
                        self.__add_route(route, route_class)

    def __load_route_class_by_file_name(self, route_file_name: str):
        try:
            # format the class in file (ClassName.ClassName)
            formatted_class = self.__format_route_class_name(route_file_name)
            # get Class Module and ClassName
            route_class, module_class_name, class_name = self.__get_integrity_route_infos(formatted_class)
            # Import the module
            __import__(module_class_name, globals(), locals(), ['*'])
            # Get the class
            _class = getattr(sys.modules[module_class_name], class_name)
            # Check if its a class
            if inspect.isclass(_class):
                # Return class
                return _class
            else:
                return None
        except:
            pass

    def __add_route(self, route, route_class):
        self.ROUTES.append((route, route_class, self._params_dict))
        address_plus_route = str(self.__kernel__.server_private_ip) + ":" + str(self.__kernel__.server_web_port) + route
        self.__console__.link("{} [WEB ROUTES] - '{}'".format(self.__classname__, address_plus_route), link=address_plus_route, end_link="", protocol="http")

    def __found_route_in_folder(self, path: str):
        # fix folder path if needed
        _path = self.__fix_folder_path_if_needed(path)
        # Add path to the system path
        self.__add_route_folder_to_system_path(_path)
        # Load all the files in path
        for f in os.listdir(_path):
            # Ignore anything that isn't a .py file and file name start by "Skill"
            if len(f) > 3 and f[-3:] == '.py':
                # get skill file name without extension
                route_file_name = f[:-3]
                # if route file not already in list
                if route_file_name not in self.ROUTES:
                    # yield the file name
                    yield route_file_name

    def __if_route_exist_in_list(self, route: str):
        # itterate every routes
        for route_in_list in self.ROUTES:
            # if route enter is in route itterate
            if route in route_in_list:
                # return True
                return True
        # else return None
        return False

    def __check_route_name(self, route):
        # check route if need to add or remove somthing in web route
        if "/skills/info" in route:
            route = route + "/*.*"
        elif "/cameras/feed" in route:
            route = route + "/*.*"
        elif "/database/table" in route:
            route = route + "/*.*"
        elif "/api/list/" in route:
            route = route.replace('/api/list/', "/api/")
        else:
            route = route
        return route

    def __create_route(self, route_path: str):
        # remove base folder of route, route_paht is like /routes/index so we remove "routes" ffolder from name
        route = route_path.split('/routes')[1]
        # remove specificies of file name to avoid doublons
        route = route.replace("admin_", "")
        route = route.replace("panel_", "")
        route = route.replace("api_", "")
        route = route.replace("_", "/")
        # if index in path
        if "index" in route_path:
            # if there are more than 2 "/"
            if route.count("/") >= 2:
                # index in sub route folder
                route = route.replace("/index", "")
            else:
                # base index
                route = route.replace("index", "")
        # return the route path (/index or /index/other)
        return route

    def __get_integrity_route_infos(self, route_file_name: str):
        route_class_path = route_file_name.split('.')
        module_class_name = '.'.join(route_class_path[:-1])
        class_name = route_class_path[-1]
        return route_class_path, module_class_name, class_name

    def __format_route_class_name(self, skill_file_name: str):
        # format skill class
        if "." not in skill_file_name:
            return skill_file_name + "." + skill_file_name
        else:
            return skill_file_name

    def __fix_folder_path_if_needed(self, path: str):
        # if not start with "/"
        if path[-1:] != '/':
            path += '/'
        return path

    def __add_route_folder_to_system_path(self, path: str):
        # Add path to the system path
        sys.path.append(path)




