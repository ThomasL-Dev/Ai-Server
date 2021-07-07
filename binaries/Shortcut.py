import os
import sys

class Shortcut:

    def __init__(self, console=None):
        self.console = console
        # file name to start program
        self.boot_file = "boot.py"
        # name of the shortcut
        self.shortcut_name = "ai_server"
        # path where execute shortcut
        self.exec_path = os.getcwd()
        # if windows
        if "win32" in sys.platform:
            # windows extension name
            self.extension = ".bat"
            # path where shortcut is saved
            self.path_to_save = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            # line writted in shortcut
            self.shortcut_value = 'cd "' + str(self.exec_path) + '"\nstart python ' + str(self.boot_file)
        # else linux
        else:
            # linux extension name
            self.extension = ".sh"
            # path where shortcut is saved
            self.path_to_save = "/home/" + os.path.expanduser('~/Desktop').replace("root", os.getlogin())
            # line writted in shortcut
            self.shortcut_value = '#!/bin/bash\ncd "' + str(self.exec_path) + '"\nsudo python3 ' + str(self.boot_file)
        # init shortcut path
        self.shortcut_path = os.path.join(self.path_to_save, self.shortcut_name + self.extension)



    def create(self):
        try:
            # if path not already exist
            if not os.path.exists(self.shortcut_path):
                try:
                    # create shortcut
                    self.__create_shortcut_file(self.shortcut_path, self.shortcut_value)
                except:
                    # if error with path create in self path
                    self.__create_safe_shortcut()

        except:
            try:
                # if any other error create in self path
                self.__create_safe_shortcut()
            except Exception as e:
                self.console.error("Error while creating shortcut -- error : " + str(e))


    def __create_shortcut_file(self, path: str, value: str):
        with open(path, "w+") as shortcut_file:
            shortcut_file.write(value)
            shortcut_file.close()
        if "linux" in sys.platform:
            os.system('chmod u+x "' + str(path) + '"')
        self.console.info("Shortcut created in '" + path + "'")


    def __create_safe_shortcut(self):
        # create shortcut self path if error with other path
        path_safe = os.path.join(os.getcwd(), self.shortcut_name + self.extension)
        if not os.path.exists(path_safe):
            self.__create_shortcut_file(path_safe, self.shortcut_value)


