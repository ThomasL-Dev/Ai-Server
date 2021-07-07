from binaries.web.obj.BasePage import BasePage
# ========================================== FIN DES IMPORTS ========================================================= #




class panel_database_table(BasePage):

    need_oauth_security = True

    def prepare(self):
        # init permission to access to this page
        self.access_permission = self.kernel.AccountsHandler.get_perm_value("admin")

        # init table name
        self.table_name = self.__get_table_name()

        try:
            # init table contents
            self.columns_table_name = self.kernel.DataBase.get_columns_name_from_table(self.table_name)
            self.table_contents = self.kernel.DataBase.get(self.table_name)
        except:
            # if error return to database tables page
            self.redirect("/admin/panel/database")



    def on_get(self):
        self.render("database_table.html",
                    ia_name=self.kernel.ia_name,
                    private_ip=self.kernel.server_private_ip,
                    public_ip=self.kernel.server_public_ip,
                    version=self.kernel.get_version(),
                    table_name=self.table_name,
                    columns_table_name=self.columns_table_name,
                    table_contents=self.table_contents,
                    )



    def on_post(self):
        self.__if_new_value_signal()
        self.__if_remove_value_signal()
        self.__if_update_value_signal()

        self.redirect("/admin/panel/database/table/{}".format(self.table_name))



    def __if_new_value_signal(self):
        new_value_signal = self.get_arg_by_name('new-value-signal')
        if new_value_signal is not None:
            self.__on_press_new_value_btn()
            # update handler account where and if needed
            self.__update_accounts_in_handler_from_web()

    def __if_remove_value_signal(self):
        remove_signal = self.get_arg_by_name('remove')
        if remove_signal is not None:
            self.__on_press_remove_btn()
            # update handler account where and if needed
            self.__update_accounts_in_handler_from_web()

    def __if_update_value_signal(self):
        update_signal = self.get_arg_by_name('update')
        if update_signal is not None:
            self.__on_press_update_btn()
            # update handler account where and if needed
            self.__update_accounts_in_handler_from_web()


    def __on_press_new_value_btn(self):
        dict = self.__generate_new_value_dict()
        # insert in db
        self.kernel.DataBase.insert(self.table_name, dict)

    def __on_press_update_btn(self):
        what = self.__check_value(self.get_arg_by_name('what'))
        what_value = self.__check_value(self.get_arg_by_name('what-value'))
        where = self.__check_value(self.get_arg_by_name('where'))
        where_value = self.__check_value(self.get_arg_by_name('where-value'))
        # update in db
        self.kernel.DataBase.update(self.table_name, what, what_value, where, where_value)

    def __on_press_remove_btn(self):
        what_value = self.__check_value(self.get_arg_by_name('what-value'))
        where = self.__check_value(self.get_arg_by_name('where'))
        where_value = self.__check_value(self.get_arg_by_name('where-value'))
        # remove in db
        self.kernel.DataBase.remove(self.table_name, where=where, where_value=where_value)


    def __get_table_name(self):
        tablename = self.request.path.split("/")[-1]
        if tablename not in self.kernel.DataBase.get_all_tables():
            self.redirect("/admin/panel/database")
        else:
            return tablename


    def __update_accounts_in_handler_from_web(self):
        # check if table name is an account table
        if "account" in self.table_name.lower():
            # if table name is account handler table name
            if self.table_name.lower() == "accounts":
                # update base account
                self.kernel.AccountsHandler.update_accounts()

            # if table name is account handler table name
            elif self.table_name.lower().startswith("ftp_"):
                # update ftp account
                self.kernel.FtpHandler.update_accounts()

            else:
                pass

    def __generate_new_value_dict(self):
        dict = {}
        for column_number in range(len(self.columns_table_name)):
            column_name = self.columns_table_name[column_number]
            # column_content = content[column_number]
            dict[column_name] = "null"
        return dict

    def __check_value(self, value):
        try:
            # try to get len of object
            len(value)
            # return value if len got
            return value
        except:
            # else caught error and return ''
            return "''"