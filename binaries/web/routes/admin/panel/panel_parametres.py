import os

from controllers.FileController import FileController

from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_parametres(BasePage):

    need_oauth_security = True

    def prepare(self):
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")



    def on_get(self):
        self.render("parametres.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    boot_file_sections=self.kernel.BootFile.get_sections(),
                    )



    def on_post(self):
        # check if remove value
        self.__if_remove_value_signal()
        # check if new value
        self.__if_new_value_signal()
        # check if value is updated
        self.__if_value_is_updated()
        # redirect to parametre page after post
        self.redirect("/admin/panel/parametres")



    def __if_remove_value_signal(self):
        # get remove signal
        rm_signal = self.get_arg_by_name("remove-signal")
        # if signal is not None
        if rm_signal is not None:
            # get option name
            option_name = self.get_arg_by_name("properties-name")
            # if option name is not None
            if option_name is not None:
                # remove option
                self.kernel.BootFile.remove_option('PROPERTIES', option_name)

    def __if_new_value_signal(self):
        # get add signal
        add_signal = self.get_arg_by_name("new-value-signal")
        # if signal is not None
        if add_signal is not None:
            # go to add parameter page
            self.redirect("/admin/panel/parametres/add")

    def __if_value_is_updated(self):
        # get section option name
        property_name = self.get_arg_by_name('properties-name')
        # get section option value
        property_value = self.get_arg_by_name('properties-value')
        # if name and value is not None
        if property_name is not None and property_value is not None:
            # update in boot file
            self.kernel.BootFile.update_value(property_name, property_value)
            # check if a debug option this need to create specific file
            self.__check_if_debug_options(property_name, property_value)

    def __check_if_debug_options(self, property_name, property_value):
        # if needed to disable update
        if property_name == "disable_update":
            file_path = os.path.join(self.kernel.PATH_FOLDER_CONFIG, "no_update.txt")
            self.__able_or_disable_property_option(property_value, file_path)

        # if needed to disable install requierement
        elif property_name == "pass_install_requierements":
            file_path = os.path.join(self.kernel.PATH_FOLDER_CONFIG, "pass_install.txt")
            self.__able_or_disable_property_option(property_value, file_path)


    def __able_or_disable_property_option(self, property_value: str, file_path: str):
        if property_value == "True" or property_value == "true":
            FileController.create_file(file_path)
        elif property_value == "False" or property_value == "false":
            FileController.remove_file(file_path)