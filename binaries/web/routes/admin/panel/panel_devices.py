from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_devices(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")
        self.access_permission += self.kernel.AccountsHandler.get_perm_value("device")



    def on_get(self):
        self.render("devices.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    device_connected_list=self.kernel.DevicesHandler.DEVICES_CONNECTED_LIST,
                    )



    def on_post(self):
        self.__if_remove_value_signal()
        self.redirect("/admin/panel/devices")



    def __if_remove_value_signal(self):
        # get value
        disconnect_client_ip = self.get_arg_by_name('remove-value')
        # if is not None
        if disconnect_client_ip is not None:
            # find de device in handler
            device = self.kernel.DevicesHandler.get_device(str(disconnect_client_ip), by="ip")
            # if device is not None
            if device is not None:
                try:
                    # disconnect the device
                    self.kernel.DevicesHandler.disconnect_device(device)
                except:
                    pass