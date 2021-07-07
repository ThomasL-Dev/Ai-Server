# pip3 install pyftpdlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.log import config_logging
import logging
config_logging(level=logging.CRITICAL)

from binaries.obj.AiObject import AiObject
from binaries.obj.HandlerObject import HandlerObject
from binaries.ConsoleDebug import ConsoleDebug

from controllers.FolderController import FolderController
# ========================================== FIN DES IMPORTS ========================================================= #


class FtpHandler(HandlerObject, AiObject):

    def __init__(self, kernel):
        HandlerObject.__init__(self, kernel)

        # Init database
        self._database = self.__kernel__.DataBase
        self._db_table = self._database.default_tables_list['ftp_accounts']

        # init ftp stockage path
        self._ftp_stockage_path = self.__kernel__.PATH_FOLDER_FTP_STORAGE
        # create ftp stockage if not exist
        FolderController.create_folder(self._ftp_stockage_path)

        # init authorizer
        self._user_authorizer = DummyAuthorizer()
        # init ftp server
        self._ftp_event_handler = _FTPEventHandler

        # init perms
        self._perms = {
            'read': "elr",
            'write': "adfmwMT",
        }

        # init accounts authorized
        self.__load_accounts_in_db()
        # create admin account at startup if not exist
        self.__create_admin_account()



    def on_handling(self):
        # init user authorizer to accept users
        self.__init_users_authorizer()
        # start the ftp server
        self.__start()



    def add_account(self, name: str, pwd: str, homedir: str, perm: str) -> None:
        # adding account to user authorizer
        self.__console__.info("{} Adding account '{}'".format(self.__classname__, name))
        self._user_authorizer.add_user(username=name, password=pwd, homedir=homedir, perm=perm)

    def update_accounts(self) -> None:
        self.__console__.info("{} Updating accounts".format(self.__classname__))
        # remove every account already stored
        self.__remove_all_account_in_ftp_handler()
        # restore every account
        self.__load_accounts_in_db()

    def stop(self) -> None:
        # close the server
        self.ftp_server.close()



    def __start(self) -> None:
        # start the server
        self.ftp_server = FTPServer(("0.0.0.0", 21), self._ftp_event_handler)
        self.ftp_server.set_reuse_addr()
        self.ftp_server.serve_forever()

    def __init_users_authorizer(self) -> None:
        # init authorizer users
        self._ftp_event_handler.authorizer = self._user_authorizer

    def __remove_in_ftp_user_handler(self, name: str) -> None:
        try:
            # remove user in user authorizer
            self._user_authorizer.remove_user(name)
        except KeyError:
            # ignore updated account
            pass

    def __remove_all_account_in_ftp_handler(self) -> None:
        # get and save users
        accs = self.__get_all_accounts_in_ftp_handler()
        # itterate every account in db
        for acc in accs:
            # remove accounts
            self.__remove_in_ftp_user_handler(acc)

    def __get_all_accounts_in_ftp_handler(self) -> list:
        accs = []
        for user in self._user_authorizer.user_table:
            accs.append(user)
        return accs

    def __get_all_accounts_in_ftp_table(self):
        # get a list of every accounts in db
        accounts = self.__kernel__.DataBase.get(self._db_table)
        # itterate accounts
        for account in accounts:
            # generator account
            # return (name, pwd, dor, perm)
            yield account

    def __load_accounts_in_db(self) -> None:
        # itterate account in db
        for account in self.__get_all_accounts_in_ftp_table():
            try:
                # get account infos
                name = account[0]
                pwd = account[1]
                dir = account[2]
                perm = account[3]
                # add to authorizer
                self.add_account(name, pwd, dir, perm)
            except:
                pass

    def __is_account_in_db(self, name: str) -> bool:
        # check if exist in db
        if self._database.get(self._db_table, what='name', where="name", where_value=name):
            return True
        else:
            return False

    def __create_admin_account(self) -> None:
        try:
            # check if admin not exist
            if not self.__is_account_in_db("admin"):
                # create account data
                name = "admin"
                password = "admin"
                dir = self.__kernel__.PATH_FOLDER_KERNEL
                perm = self._perms['read'] + self._perms['write']
                # data dict
                account = {'name': name, 'password': password, 'dir': dir, 'perm': perm}
                # insert in db
                self.__kernel__.DataBase.insert(self._db_table, account)
                # insert in user authorizer
                self._user_authorizer.add_user(username=name, password=password, homedir=dir, perm=perm)
        except:
            pass

    @staticmethod
    def get_permissions_description() -> str:
        return """
        Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
         - "r" = retrieve file from the server (RETR command)
        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
         - "M" = change file mode (SITE CHMOD command)
        """




class _FTPEventHandler(FTPHandler):

    def on_connect(self):
        console_log = ConsoleDebug()
        console_log.info("{}:{} Trying to connect to FTP Server".format(self.remote_ip, self.remote_port))


    def on_disconnect(self):
        console_log = ConsoleDebug()
        console_log.info("{}:{} Disconnected from FTP Server".format(self.remote_ip, self.remote_port))


    def on_login(self, username):
        console_log = ConsoleDebug()
        console_log.info("FTP user '{}' connected".format(str(username).capitalize()))


    def on_logout(self, username):
        console_log = ConsoleDebug()
        console_log.info("FTP user '{}' disconnected".format(str(username).capitalize()))





