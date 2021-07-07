import os

from binaries.web.obj.BasePage import BasePage
from controllers.DateController import DateController
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_logs(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")



    def on_get(self):
        self.render("logs.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    log_lines=self.__get_all_lines_from_file()
                    )



    def __get_all_lines_from_file(self):
        logs = self.__get_log_file_from_web()
        if logs is not None:
            with open(logs, "r+") as log_file:
                lines = log_file.readlines()
                log_file.close()
            return lines
        return ""

    def __get_log_file_from_web(self):
        logs_folder = os.path.join(os.getcwd(), ".Logs")
        files = os.listdir(logs_folder)
        for log_file in files:
            if DateController.get_date().replace("/", "-") in log_file:
                return os.path.join(logs_folder, log_file)
        return None
