import datetime
import os
import sys
from controllers.FolderController import FolderController
from controllers.FileController import FileController
from controllers.TimeController import TimeController
from controllers.DateController import DateController
# ========================================== FIN DES IMPORTS ========================================================= #

class Logger:

    def __init__(self):
        self.log_folder = os.path.join(os.getcwd(), ".Logs")


    def log(self, string: str, startwith: str="", endwith: str=""):
        log = "{}[LOG] {}{}".format(startwith, string, endwith)
        self.__write_in_log_file(log)

    def info(self, string: str, startwith: str="", endwith: str=""):
        log = "{}[INFO] {}{}".format(startwith, string, endwith)
        self.__write_in_log_file(log)

    def error(self, string: str):
        log = "[ERROR] {}".format(string)
        self.__write_in_log_file(log)



    def __write_in_log_file(self, log: str):
        # check logs folder exist
        FolderController.if_folder_exist(self.log_folder, create_if_not_exist=True)
        # init log file name & path
        log_file_path = self.__init_log_file_path()
        # check log file & create if necessary
        self.__check_if_log_file_exist(log_file_path)
        # write in log file
        with open(log_file_path, "a+") as log_file:
            log = self.__add_date_to_log_string(log)
            if "win32" in sys.platform:
                log_file.write("\n" + log)
            else:
                log_file.write(log + "\n")
            log_file.close()

    def __init_log_file_path(self):
        log_file_name = str("log-{}.txt".format(DateController.get_date().replace("/", "-")))
        log_file_path = os.path.join(self.log_folder, log_file_name)
        return log_file_path

    def __add_date_to_log_string(self, log: str):
        date = DateController.get_date()
        time = TimeController.get_time()
        return "[{}-{}] ".format(date, time) + log

    def __check_if_log_file_exist(self, file_name: str):
        # check if log file exist
        if not FileController.if_file_exist(file_name):
            self.__create_log_file(file_name)

    def __create_log_file(self, file_name: str):
        # create log file
        _string = "### [ LOGS DU {} ] ###".format(DateController.get_date().upper())
        with open(file_name, "w+") as log_file:
            log_file.write("#" * len(_string) + "\n")
            log_file.write(_string + "\n")
            log_file.write("#" * len(_string) + "\n")
            log_file.close()