import os
import sqlite3
# ========================================== FIN DES IMPORTS ========================================================= #


class DataBase:
    # init dbs list
    _db_file_name = "Ai.db"

    ### DEFAULT TABLE RELATIVE ###
    default_tables_list = {
        'accounts': "accounts",
        'devices_registred': "devices_registred",
        'ftp_accounts': "ftp_accounts",
                           }

    ### DEFAULT REQUEST TABLE RELATIVE ###
    _REQUEST_SQL_CREATE_ACCOUNT_TABLE = """
                     CREATE TABLE IF NOT EXISTS """ + default_tables_list['accounts'] + """(
                        name TEXT PRIMARY KEY UNIQUE,
                        password TEXT,
                        perm TEXT,
                        active TEXT
                        )"""
    _REQUEST_SQL_INSERT_INTO_ACCOUNT_TABLE = "INSERT INTO " + default_tables_list['accounts'] + "(name, password, perm) VALUES(:name, :password, :perm, :active)"

    _REQUEST_SQL_CREATE_DEVICE_REGISTRED_TABLE = """
                     CREATE TABLE IF NOT EXISTS """ + default_tables_list['devices_registred'] + """(
                        ip TEXT PRIMARY KEY UNIQUE,
                        name TEXT,
                        alias TEXT,
                        mac TEXT,
                        vendor TEXT
                        )"""
    _REQUEST_SQL_INSERT_INTO_DEVICE_REGISTRED_TABLE = "INSERT INTO " + default_tables_list['devices_registred'] + "(ip, name, alias, mac, vendor) VALUES(:ip, :name, :alias, :mac, :vendor)"

    _REQUEST_SQL_CREATE_FTP_ACCOUNT_TABLE = """
                     CREATE TABLE IF NOT EXISTS """ + default_tables_list['ftp_accounts'] + """(
                        name TEXT PRIMARY KEY UNIQUE,
                        password TEXT,
                        dir TEXT,
                        perm TEXT
                        )"""
    _REQUEST_SQL_INSERT_INTO_FTP_ACCOUNT_TABLE = "INSERT INTO " + default_tables_list['ftp_accounts'] + "(name, password, dir, perm) VALUES(:name, :password, :dir, :perm)"
    # ===


    REQUEST_SQL_UPDATE = "UPDATE {} SET {} = '{}' WHERE {} = '{}'"
    REQUEST_SQL_REMOVE = "DELETE from {} where {} = '{}'"


    def __init__(self, kernel, db_folder_path=None):
        # init db folder
        self._DB_FOLDER_PATH = db_folder_path
        # init path file
        self.db_path = os.path.join(self._DB_FOLDER_PATH, self._db_file_name)
        # init db by creating tables if they dont exist
        self.__create_default_tables()



    def insert(self, table_name: str, dict: dict=None):
        # generate a new insert reques with table name
        insert_request = self.__generate_insert_request(table_name)
        # execute request
        self.__execute(insert_request, dict)

    def update(self, table_name: str, what: str, what_value: str, where: str, where_value: str):
        # execute request update request (in table, what to update with value, where with where value)
        # ex : update in "table" "name" "oldValue" where "name" is "newValue"
        self.__execute(self.REQUEST_SQL_UPDATE.format(table_name, what, what_value, where, where_value))

    def get(self, table_name: str, what='*', where=None, where_value=None):
        # connect to db
        db = self.__connect_to_db()
        # init cursor
        cursor = db.cursor()
        try:
            # if value to find and value to update is None
            if where is None and where_value is None:
                # get what we need in table name
                cursor.execute("SELECT {} FROM {}".format(what, table_name))
                # return values found
                return cursor.fetchall()
            # else execute request with value specific to find
            else:
                cursor.execute('SELECT {} FROM {} WHERE {} = "{}"'.format(what, table_name, where, where_value))
                # return values found
                return cursor.fetchone()[0]
            # close cursor
            cursor.close()
            # close db connection
            db.close()
        except:
            pass
        return None

    def remove(self, table_name: str, where=None, where_value=None):
        # execute remove request where "value" is "value"
        self.__execute(self.REQUEST_SQL_REMOVE.format(table_name, where, where_value))

    def get_columns_name_from_table(self, table_name: str):
        # conenct to db
        db = self.__connect_to_db()
        # select every tables
        cursor = db.execute('select * from {}'.format(table_name))
        # list every table names
        names = list(map(lambda x: x[0], cursor.description))
        # close cursor
        cursor.close()
        # close db connection
        db.close()
        # return tables name
        return names

    def get_all_tables(self):
        # init tables list
        out = []
        # conenct to db
        db = self.__connect_to_db()
        # init cursor
        cursor = db.cursor()
        # execute select table request
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # get everyuthing
        _cur = cursor.fetchall()
        # itterate tables
        for table in _cur:
            try:
                # add table name to list
                out.append(table[0])
            except:
                continue
        # cose cursor
        cursor.close()
        # close db connection
        db.close()
        # return table list
        return out



    def __execute(self, requete: str, slot=None):
        try:
            db = self.__connect_to_db()
            if slot is None:
                db.execute(requete)
            else:
                db.execute(requete, slot)
            db.commit()
            db.close()
        except Exception as e:
            pass

    def __generate_insert_request(self, table_name: str):
        columns_name = self.get_columns_name_from_table(table_name)
        sql = "INSERT INTO {}(".format(table_name)

        for column in columns_name:
            sql += column + ", "
        sql += ")"

        sql += " VALUES("
        for column in columns_name:
            sql += ":" + column + ", "
        sql += ")"

        sql = sql.replace(", )", ")")
        return sql

    def __create_default_tables(self):
        self.__execute(self._REQUEST_SQL_CREATE_ACCOUNT_TABLE)
        self.__execute(self._REQUEST_SQL_CREATE_DEVICE_REGISTRED_TABLE)
        self.__execute(self._REQUEST_SQL_CREATE_FTP_ACCOUNT_TABLE)

    def __connect_to_db(self):
        return sqlite3.connect(self.db_path)