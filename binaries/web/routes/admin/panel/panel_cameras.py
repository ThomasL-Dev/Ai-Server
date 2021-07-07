from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_cameras(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")
        self.access_permission += self.kernel.AccountsHandler.get_perm_value("camera")



    def on_get(self):
        self.render("cameras.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    cameras_list=self.kernel.CamerasHandler.CAMERAS_LIST
                    )



    def on_post(self):
        self.__if_new_value_signal()
        self.__if_remove_value_signal()
        # if other post signal return to camera page
        self.redirect("/admin/panel/cameras")



    def __if_new_value_signal(self):
        add_signal = self.get_arg_by_name("new-value-signal")
        if add_signal is not None:
            self.redirect("/admin/panel/cameras/add")

    def __if_remove_value_signal(self):
        rm_signal = self.get_arg_by_name('remove-value')
        if rm_signal is not None:
            self.kernel.CamerasHandler.remove_camera(str(rm_signal))