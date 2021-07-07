from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_skills(BasePage):

    need_oauth_security = True

    def prepare(self):
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")
        self.access_permission += self.kernel.AccountsHandler.get_perm_value("skill")



    def on_get(self):
        self.render("skills.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    skill_list=self.kernel.SkillHandler.SKILLS_LIST,
                    )



    def on_post(self):
        self.__if_remove_value_signal()
        self.redirect("/admin/panel/skills")



    def __if_remove_value_signal(self):
        rm_value = self.get_arg_by_name('remove-value')
        if rm_value is not None:
            self.kernel.SkillHandler.remove_skill(str(rm_value))


