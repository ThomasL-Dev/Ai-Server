from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_database(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")



    def on_get(self):
        self.render("database.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    db_tables=self.kernel.DataBase.get_all_tables(),
                    )
