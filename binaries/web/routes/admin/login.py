from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class login(BasePage):

    def on_get(self):
        if self.oauth_security_system():
            self.redirect("/admin/panel")
        else:
            self.render("login.html", ia_name=self.kernel.ia_name)


    def on_post(self):
        id = self.get_arg_by_name("id")
        pwd = self.get_arg_by_name("pwd")

        self.redirect("/admin/auth?id={}&pwd={}".format(id, pwd))
