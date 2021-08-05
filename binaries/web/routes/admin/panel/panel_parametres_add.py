from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_parametres_add(BasePage):

    need_oauth_security = True

    def on_get(self):
        self.render("parametres_add.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    )



    def on_post(self):
        self.__if_add_button_is_triggered()
        # if other post signal return to camera page
        self.redirect("/admin/panel/cameras")



    def __if_add_button_is_triggered(self):
        # check if button add is clicked
        add = self.get_arg_by_name("add")
        # if btn add is not None
        if add is not None:
            # get cam name
            name = self.get_arg_by_name("name")
            # get cam index
            index = self.get_arg_by_name("value")

            self.__if_option_info_are_ok(name, index)

    def __if_option_info_are_ok(self, name, index):
        if name is None and index is None:
            self.redirect("/admin/panel/parametres/add")
        else:
            self.__add_camera_from_web(name, index)

    def __add_camera_from_web(self, option_name: str, value: str):
        self.kernel.BootFile.add_option(option_name, value)
        self.redirect("/admin/panel/parametres")
