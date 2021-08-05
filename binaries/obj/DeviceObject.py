import select
import time
from threading import Thread
import requests
import socket
from getmac import get_mac_address

from binaries.builders.RequestBuilder import RequestBuilder
from binaries.obj.AiObject import AiObject

from controllers.TimeController import TimeController
from controllers.DateController import DateController
# ========================================== FIN DES IMPORTS ========================================================= #




class DeviceObject(Thread, AiObject):

    def __init__(self, kernel, type, device_socket, device_address):
        Thread.__init__(self)
        AiObject.__init__(self, kernel)
        self.setDaemon(True)

        # Init database
        self._database = self.__kernel__.DataBase
        self._db_table = self._database.default_tables_list['devices_registred']
        # init client data
        self._data_from_client = None
        # init connection statut
        self._connected_to_server = True
        # getting client socket
        self._client_address = device_address
        # gettable device infos
        self._socket = device_socket
        self._type = str(type)
        self._ip = str(self._client_address[0])
        self._name = self.get_name()
        self._alias = self.get_alias()
        self._mac = self.__get_mac()
        self._vendor = self.__get_vendor()



    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'type={self.get_type()!r}, '
                f'ip={self.get_ip()!r}, '
                f'name={self.get_name()!r}, '
                f'alias={self.get_alias()!r}, '
                f'mac={self.get_mac()!r}, '
                f'vendor={self.get_vendor()!r}, '
                f'socket={self.get_socket()!r}'
                f')')



    def run(self):
        # show connection infos
        self.__console__.info("{} '{}' ({}) Connected to server".format(self.__classname__, self._name.capitalize(), self._ip), color="green")
        # send to discord
        self.__kernel__.DiscordHandler.send_log("'{}' ({}) connected".format(self.get_name().capitalize(), self.get_ip()), self.__kernel__.BootFile.get_value("discord_channel_log_device"))
        # running communication handler
        self.__console__.info("{} Handling communication for '{}' ({})".format(self.__classname__, self._name.capitalize(), self._ip))
        # start the device data handling
        while self._connected_to_server:
            # if socket is not None
            if self._socket:
                # Check if the client is still connected and if data is available:
                rdy_read, rdy_write, sock_err = self.__check_if_data_available()
                # if data is not 'dead' (socket closed)
                if len(rdy_read) > 0:
                    try:
                        # getting msg from device
                        self._data_from_client = self._socket.recv(1024).decode('utf8')
                        # if len is 0 socket is dead
                        if len(self._data_from_client) == 0:
                            self.disconnect()
                        else:
                            # else read msg
                            device_receiv = str(self._data_from_client)

                            # DO CODE ACTION
                            # RECEIVE PING
                            if "code:ping" in device_receiv:
                                # SEND PONG
                                self._socket.send("code:{}".format("pong").encode("utf8"))
                            else:
                                # Do a new request
                                RequestBuilder(self.__kernel__, self._name, device_receiv)

                    except Exception as e:
                        self.disconnect()
                time.sleep(0.15)
            else:
                self.__stop_handling()
        self.__close_socket()



    def get_socket(self) -> str:
        return self._socket

    def get_type(self) -> str:
        return self._type

    def get_ip(self) -> str:
        return self._ip

    def get_name(self) -> str:
        # get name in db
        name = self._database.get(self._db_table, what='name', where='ip', where_value=self._ip)
        if name is not None:
            # return name if not null in db
            return name
        else:
            try:
                # return name with socket if null in db
                return str(socket.gethostbyaddr(self._ip)[0]).split(".")[0]
            except:
                return "Inconnu"

    def get_alias(self) -> str:
        # get alias in db
        alias = self._database.get(self._db_table, what='alias', where='ip', where_value=self._ip)
        if alias is not None:
            # return alias if not null in db
            return alias
        else:
            return 'Aucun'

    def get_mac(self) -> str:
        # return mac
        return self._mac

    def get_vendor(self) -> str:
        # return vendor
        return self._vendor


    def update_name(self, value: str) -> None:
        # if value is not Null
        if value is not None or value != '':
            # store the name with old name
            prev_name = self._name
            # set the object name with new value
            self._name = value
            # update in db
            self._database.update(what="name", new_value=value, target_ip=self._ip)
            self.__console__.info("{} Name updated to '{}'".format(self.__classname__, prev_name.capitalize(), value.capitalize()))

    def update_alias(self, value: str) -> None:
        # if value is not Null
        if value is not None or value != '':
            # store the alias with old alias
            prev_alias = self._alias
            # set the object alias with new value
            self._alias = value
            # update in db
            self._database.update(what="alias", new_value=value, target_ip=self._ip)
            self.__console__.info("{} Alias updated to '{}'".format(self.__classname__, prev_alias.capitalize(), value.capitalize()))


    def disconnect(self) -> None:
        # show disconnection info
        self.__console__.info("{} '{}' ({}) Disconnected from server".format(self.__classname__, self._name.capitalize(), self._ip), color="red")
        # send to discord
        self.__kernel__.DiscordHandler.send_log("'{}' ({}) disconnected".format(self.get_name().capitalize(), self.get_ip()), self.__kernel__.BootFile.get_value("discord_channel_log_device"))
        # close the socket
        self.__close_socket()
        # stop handling new msg
        self.__stop_handling()
        # remove obj from list
        self.__remove_device_from_connected_list()


    def __get_mac(self) -> str:
        # get mac address
        mac = get_mac_address(ip=self._ip)
        if mac is not None:
            # return mac if not null
            return mac
        else:
            return "00:00:00:00:00:00"

    def __get_vendor(self) -> str:
        # setting url to get vendor
        url = "https://api.macvendors.com/" + self._mac
        try:
            # get vendor text
            s = str(requests.get(url).text)
            if "errors" in s:
                return "Vendor not found"
            else:
                return s
        except:
            return "Vendor not found"


    def __close_socket(self) -> None:
        # close the socket if not null
        if self._socket:
            self._socket.close()

    def __stop_handling(self) -> None:
        # stop handling connection
        self._connected_to_server = False

    def __check_if_data_available(self):
        try:
            # return datas if socket is not dead
            rdy_read, rdy_write, sock_err = select.select([self._socket, ], [self._socket, ], [], 5)
            return rdy_read, rdy_write, sock_err

        except select.error as err:
            self.__stop_handling()
            return

    def __remove_device_from_connected_list(self) -> None:
            self.__kernel__.DevicesHandler.DEVICES_CONNECTED_LIST.remove(self)