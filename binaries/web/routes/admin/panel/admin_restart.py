from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class admin_restart(BasePage):

    local_connexion_only = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")



    def on_get(self):
        self.redirect("/")
        self.kernel.restart()

    def on_post(self):
        self.redirect("/")
        self.kernel.restart()




