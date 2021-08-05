import os
import sys
import time

from binaries.Shortcut import Shortcut
from binaries.ConsoleDebug import ConsoleDebug
from binaries.DataBase import DataBase
from binaries.BootFile import BootFile
from binaries.Logger import Logger
log = Logger()

# handlers
from binaries.handlers.AccountHandler import AccountHandler
from binaries.handlers.DiscordHandler import DiscordHandler
from binaries.handlers.SkillHandler import SkillHandler
from binaries.handlers.RequestHandler import RequestHandler
from binaries.handlers.DevicesHandler import DevicesHandler
from binaries.handlers.WebHandler import WebHandler
from binaries.handlers.FtpHandler import FtpHandler
from binaries.handlers.CamerasHandler import CamerasHandler

#obj
from binaries.obj.UpdaterObject import UpdaterObject

# controllers
from controllers.FolderController import FolderController
from controllers.FileController import FileController
from controllers.NetworkController import NetworkController
# ========================================== FIN DES IMPORTS ========================================================= #



class Kernel:
    # SERVER IPs
    server_public_ip = None
    server_private_ip = None
    # PATHS
    PATH_FOLDER_KERNEL = os.getcwd()
    # folder path for handlers
    PATH_FOLDER_STORAGE = os.path.join(PATH_FOLDER_KERNEL, ".stockage")
    PATH_FOLDER_CONFIG = os.path.join(PATH_FOLDER_KERNEL, ".cfg")
    PATH_FOLDER_DATABASE = os.path.join(PATH_FOLDER_KERNEL, ".db")
    # general path
    PATH_FOLDER_BINARIES = os.path.join(PATH_FOLDER_KERNEL, "binaries")
    PATH_FOLDER_FTP_STORAGE = os.path.join(PATH_FOLDER_STORAGE, "ftp")
    PATH_FOLDER_SKILLS = os.path.join(PATH_FOLDER_KERNEL, "skills")
    # files
    PATH_FILE_BOOT = os.path.join(PATH_FOLDER_CONFIG, "boot.ini")
    PATH_FILE_VERSION = os.path.join(PATH_FOLDER_KERNEL, "version.txt")



    def __init__(self):
        self._class_name = "[{}]".format(self.__class__.__name__)

        # init server ip's
        self.server_public_ip = NetworkController.public_ip()
        self.server_private_ip = NetworkController.private_ip()

        # init console
        self.console = ConsoleDebug()
        self.console.set_console_size()
        self.console.clear_console()
        log.log("Starting server ...", startwith="\n")

        # create shortcut if not exist
        shortcut = Shortcut(console=self.console)
        shortcut.create()

        # create needed handlers folders if they didnt exist
        FolderController.create_folder(self.PATH_FOLDER_STORAGE)
        FolderController.create_folder(self.PATH_FOLDER_CONFIG)
        FolderController.create_folder(self.PATH_FOLDER_DATABASE)

        # init boot file config
        self.BootFile = BootFile(self.PATH_FILE_BOOT)
        self.ia_name = str(self.BootFile.get_value('ai_name').capitalize())
        self.discord_token = self.BootFile.get_value('discord_token')
        self.server_port = int(self.BootFile.get_value('server_port'))
        self.server_web_port = self.server_port + 1

        # init database
        self.DataBase = DataBase(kernel=self, db_folder_path=self.PATH_FOLDER_DATABASE)

        # init handlers
        self.WebHandler = WebHandler(self, port=int(self.server_web_port))
        self.DiscordHandler = DiscordHandler(self, token=self.discord_token)
        self.AccountsHandler = AccountHandler(self)
        self.SkillHandler = SkillHandler(self, skill_path=self.PATH_FOLDER_SKILLS)
        self.RequestHandler = RequestHandler(self)
        self.DevicesHandler = DevicesHandler(self, port=int(self.server_port))
        self.FtpHandler = FtpHandler(self)
        self.CamerasHandler = CamerasHandler(self)

        # start Updater
        self._version_file_url = "https://www.dropbox.com/s/jtgs1k6z23fm44c/server_version.txt?dl=1"
        self._zip_folder_url = "https://www.dropbox.com/s/5ggzgp8rjacea1b/Server.zip?dl=1"
        self.Updater = UpdaterObject(kernel=self, dropbox_url_version_file=self._version_file_url,
                                     dropbox_url_binaries_zip=self._zip_folder_url)
        self.Updater.update()
        self.console.kernel("Version : " + self.get_version())



    def start(self) -> None:
        # set console name & size
        self.console.set_title(self.ia_name)
        self.console.set_console_size()
        # start webhandler for infos
        self.WebHandler.start()
        # start else handlers
        self.AccountsHandler.start()
        self.DiscordHandler.start()
        self.SkillHandler.start()
        self.DevicesHandler.start()
        self.RequestHandler.start()
        self.FtpHandler.start()
        self.CamerasHandler.start()
        # join the thread to not close the program
        self.DiscordHandler.join()

    def stop(self) -> None:
        # STOPPING THE SERVER
        self.console.info('{} Stopping server'.format(self._class_name))
        self._action_before_stopping_server()
        # stop program
        os._exit(1)

    def restart(self) -> None:
        self.console.info('{} Restarting server'.format(self._class_name))
        self._action_before_stopping_server()
        # restart program
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def restart_physic_machine(self) -> None:
        self.console.info('{} Restarting physical server'.format(self._class_name))
        self._action_before_stopping_server()
        # restart machine
        import subprocess
        try:
            if sys.platform == "linux":
                subprocess.call(["reboot"])

            elif sys.platform == "win32":
                subprocess.call(["shutdown", "/r", "/t", "15"])
        except Exception as e:
            pass



    def get_version(self) -> str:
        return self.Updater.get_installed_version()



    def _action_before_stopping_server(self) -> None:
        # ACTIONS TO DO BEFORE STOPPING SERVER #
        # disconnect every device connected
        self.DevicesHandler.disconnect_all_devices()
        # stopping every cams
        self.CamerasHandler.stop_all_cameras()
        # remove cache
        self.__remove_cache()


    def __remove_cache(self) -> None:
        self.console.info('{} Removing cache'.format(self._class_name))
        # itterate every dir and file
        for dir, dirname, filenames in os.walk(self.PATH_FOLDER_KERNEL):
            # if cache folder
            if "__pycache__" in dir.split("/")[-1:]:
                # itterate every files in cache folder
                for filename in filenames:
                    # remove file
                    FileController.remove_file(os.path.join(dir, filename))
                # when all files removed remove cache folder
                FolderController.remove_folder(dir)

