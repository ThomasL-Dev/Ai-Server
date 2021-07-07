from binaries.obj.AiObject import AiObject
from binaries.obj.AccountObject import AccountObject
from binaries.obj.HandlerObject import HandlerObject
# ========================================== FIN DES IMPORTS ========================================================= #


class AccountHandler(HandlerObject, AiObject):

    def __init__(self, kernel):
        HandlerObject.__init__(self, kernel)
        # init account list
        self.ACCOUNTS_LIST = []
        # Init database
        self._database = self.__kernel__.DataBase
        self._db_table = self._database.default_tables_list['accounts']

        # init perms
        self._perms = {
            'admin': "admin",
            'camera': "camera",
            'device': "device",
            'skill': "skill",
        }

        # load accounts at startup
        self.__load_accounts_in_db()
        # create admin account at startup if not exist
        self.__create_admin_account()



    def add_account(self, name: str, pwd: str, perm: str='', active: str="true") -> None:
        # check if already in list or not
        if not self.__is_in_list(name):
            self.__console__.info("{} Adding account '{}'".format(self.__classname__, name))
            # add to db
            self.__add_account_to_db(name, pwd, perm, active)
            # add to list
            self.__add_account_to_list(name, pwd, perm, active)

    def update_accounts(self) -> None:
        self.__console__.info("{} Updating accounts".format(self.__classname__))
        # remove every accounts
        self.__remove_all_accounts_in_list()
        # reload every accounts
        self.__load_accounts_in_db()


    def is_auth(self, acc_name: str, acc_pwd: str) -> bool:
        # itterate account in list
        acc = self.get_account(acc_name)
        # if acc object is not None
        if acc is not None:
            # if account and password is egal to acc stored
            if acc_name == acc.get_name() and acc_pwd == acc.get_password() and acc.is_active():
                    # return True
                    self.__console__.info("{} '{}' Account authorized with password '{}'".format(self.__classname__, acc_name, acc_pwd))
                    # send to discord
                    self.__kernel__.DiscordHandler.send_log("Account '{}' connected".format(acc_name), self.__kernel__.BootFile.get_value("discord_channel_log_account"))
                    return True
        # return False
        self.__console__.error("{} '{}' Account unauthorized with password '{}'".format(self.__classname__, acc_name, acc_pwd))
        self.__kernel__.DiscordHandler.send_log("Account '{}' tried to connect".format(acc_name), self.__kernel__.BootFile.get_value("discord_channel_log_account"))
        return False


    def have_perm(self, account_name: str, perm_name: str) -> bool:
        # find acc obj
        account = self.get_account(account_name)
        # if acc is not None
        if account is not None:
            # if perm enter is in account perm
            if account.get_perm() in perm_name:
                # return True
                self.__console__.info("{} '{}' Account have permission".format(self.__classname__, account_name, perm_name))
                return True
        # else return False
        self.__console__.error("{} '{}' Account have not C".format(self.__classname__, account_name, perm_name))
        return False


    def get_account(self, account_name: str) -> AccountObject:
        # itterate account in list
        for account in self.ACCOUNTS_LIST:
            # if account name is eegal to name enter
            if account_name == account.get_name():
                # return account object
                return account
        # else return None
        return None

    def get_perm_value(self, perm_name: str) -> str:
        try:
            self.__console__.info("{} Getting '{}' permission value ".format(self.__classname__, perm_name))
            return self._perms[perm_name]
        except:
            self.__console__.error("{} '{}' permission not found ".format(self.__classname__, perm_name))
            return None

    def get_perms(self) -> list:
        out = []
        self.__console__.info("{} 'Getting permissions".format(self.__classname__))
        # itterate perms
        for perm in self._perms:
            # add perm
            out.append(perm)
        # return perms name without the value of the perm
        return out



    def __is_in_list(self, account_name: str) -> bool:
        # find acc obj
        account = self.get_account(account_name)
        # if acc is not None
        if account is not None:
            # if account name is eegal to name enter
            if account_name == account.get_name():
                # return True
                return True
        # else return False
        return False

    def __add_account_to_db(self, name: str, pwd: str, perm: str, active: str) -> None:
        dict_data = {'name': name, 'password': pwd, 'perm': perm, "active": active}
        self._database.insert(self._db_table, dict_data)

    def __add_account_to_list(self, name: str, pwd: str, perm: str, active: str) -> None:
        # add account to list
        self.ACCOUNTS_LIST.append(AccountObject(self.__kernel__, name, pwd, perm, active))

    def __remove_account_from_list(self, account_name: str) -> None:
        # get account object
        account = self.get_account(account_name)
        # if object is not none
        if account is not None:
            # remove account from list
            self.ACCOUNTS_LIST.remove(account)

    def __remove_all_accounts_in_list(self) -> None:
        # remove everything in list
        self.ACCOUNTS_LIST.clear()

    def __load_accounts_in_db(self) -> None:
        # itterate account in db
        for account in self.__get_all_account_in_account_table():
            try:
                # get account infos
                name = account[0]
                pwd = account[1]
                perm = account[2]
                actif = account[3]
                # add to list
                self.add_account(name, pwd, perm, actif)
            except:
                pass

    def __get_all_account_in_account_table(self) -> None:
        # get a list of every accounts in db
        accounts = self.__kernel__.DataBase.get(self._db_table)
        # itterate accounts
        for account in accounts:
            # generator account
            # return (name, pwd, perm, token)
            yield account


    def __create_admin_account(self) -> None:
        # create admin account if dont exist
        name = "admin"
        pwd = "admin"
        perm = self.get_perm_value("admin")
        self.add_account(name, pwd, perm)