import logging
# remove logging error from updating image
hn = logging.NullHandler()
hn.setLevel(logging.NOTSET)
logging.getLogger("tornado.general").addHandler(hn)
logging.getLogger("tornado.general").propagate = False
logging.getLogger("tornado.application").addHandler(hn)
logging.getLogger("tornado.application").propagate = False

from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_cameras_feed(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")
        self.access_permission += self.kernel.AccountsHandler.get_perm_value("camera")
        # check the camera if is handler or not
        self.__check_getted_camera()



    def on_get(self):
        self.render("camera_feed.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    camera_name=self.__get_camera_name_in_route().replace("_", " "),
                    camera=self.camera,
                    )



    def __check_getted_camera(self):
        # get the cam object
        self.camera = self.__get_camera_from_web()
        # if camera not found in handler
        if self.camera is None:
            # redirect to cameras page
            self.redirect("/admin/panel/cameras")

    def __get_camera_from_web(self):
        # return
        return self.kernel.CamerasHandler.get_camera_by_name(self.__get_camera_name_in_route())

    def __get_camera_name_in_route(self):
        # split the url
        url_splitted = self.request.path.split("/")
        # camera name is the last value of splitted url
        return url_splitted[-1]