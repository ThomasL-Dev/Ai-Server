from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #


class auth(BasePage):

    def prepare(self):
        self.id = self.get_arg_by_name("id")
        self.pwd = self.get_arg_by_name("pwd")



    def on_get(self):
        if self.kernel.AccountsHandler.is_auth(self.id, self.pwd):
            self.set_secure_cookie("account-connected-cookies", self.id, expires_days=0.008)
            self.redirect("/admin/panel")

        else:
            self.redirect("/admin/login")
