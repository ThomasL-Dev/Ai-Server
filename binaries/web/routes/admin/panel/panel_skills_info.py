from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #


class panel_skills_info(BasePage):

    need_oauth_security = True

    def prepare(self):
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")
        self.access_permission += self.kernel.AccountsHandler.get_perm_value("skill")

        # prepare skill needed information
        # get skill name
        self.skill_name = self.__get_skill_name_from_route()
        # get skill object
        self.skill = self.kernel.SkillHandler.get_skill_by_name(self.skill_name)
        # if not None
        if self.skill is not None:
            # get skill vars
            self.skill_infos = self.__get_skill_vars()
        else:
            # else redirect to skilsl page
            self.redirect("/admin/panel/skills")



    def on_get(self):
        self.render("skill_info.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    skill_name=self.skill_name,
                    skill=self.skill,
                    skill_infos=dict(self.skill_infos))



    def __get_skill_name_from_route(self):
        return self.request.path.split("/")[-1]

    def __get_skill_vars(self):
        dict = {}
        for skill_var in dir(self.skill):
            if not callable(getattr(self.skill, skill_var)) and not skill_var.startswith("__") and "kernel" not in skill_var and "_name" not in skill_var:
                dict[skill_var] = getattr(self.skill, skill_var)
        return dict