import socket
import time

from binaries.obj.HandlerObject import HandlerObject
from binaries.obj.DeviceObject import DeviceObject
# ========================================== FIN DES IMPORTS ========================================================= #


class DevicesHandler(HandlerObject):

    def __init__(self, kernel, ip='', port=33000):
        HandlerObject.__init__(self, kernel)

        # init devices list
        self.DEVICES_CONNECTED_LIST = []

        # Init database
        self._database = self.__kernel__.DataBase
        self._db_table = self._database.default_tables_list['devices_registred']
        # Init socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(1)
        # Init server adresse (ip:port)
        self._host = ip
        self._port = port
        # init max devices autorized to connect
        self._max_devices_authorized = self.__get_max_device_authorized()
        # Statut server if is closed or not
        self._waiting_device_connection = True
        # Bind socket to adresse & listen max connection
        self.__bind_adress()



    def on_handling(self):
        # Accept an incoming connection
        self.__console__.info("{} Waiting devices to connect".format(self.__classname__))

        while self._waiting_device_connection:
            # receiving socket and address
            device_socket, device_address = self.__accept_incoming_connection()
            # if socket is valid
            if device_socket:
                # new device connected
                try:
                    # getting header from device who trying to connect
                    incoming_header = device_socket.recv(32).decode("utf8")
                    # getting type from header
                    device_type = self.__get_type_from_header(incoming_header)
                    # if device in not None and valid
                    if device_type is not None:
                        # new device accepted and let it connect
                        self.__on_new_device_connected(device_socket, device_address, device_type)
                    else:
                        self.__console__.error("{} Device '{}' have a wrong header".format(self.__classname__, device_address[0]))
                        continue
                except:
                    continue
                time.sleep(0.7)

        # closing server when waiting is Null
        self.__stopping_handler()



    def get_device(self, target: str, by: str="name") -> DeviceObject:
        self.__console__.info("{} Getting device '{}' object".format(self.__classname__, target))
        # itterate devices
        for device in self.DEVICES_CONNECTED_LIST:
            # check by ip or name
            if by == "name":
                # if target is egal to device name
                if target in str(device.get_name()):
                    # return device
                    self.__console__.info("{} Device '{}' object getted".format(self.__classname__, target))
                    return device

            elif by == "ip":
                # if target is egal to device ip
                if target == str(device.get_ip()):
                    # return device
                    self.__console__.info("{} Device '{}' object getted".format(self.__classname__, target))
                    return device
            else:
                pass
        # return None
        self.__console__.info("{} Device '{}' object not found".format(self.__classname__, target))
        return None

    def disconnect_device(self, device: DeviceObject) -> None:
        # disconnecting the device
        try:
            self.__console__.info("{} Disconnecting device '{}'".format(self.__classname__, device.get_name()))
            device.disconnect()
        except Exception as e:
            self.__console__.error("{} Error while disconnecting device '{}'".format(self.__classname__, device.get_name(), e))
            pass

    def disconnect_all_devices(self) -> None:
        self.__console__.info("{} Disconnecting every devices".format(self.__classname__))
        for device in self.DEVICES_CONNECTED_LIST:
            self.disconnect_device(device)

    def stop(self) -> None:
        # stop waiting for device
        self.__stop_handling_devices()
        # stop the handler
        self.__stopping_handler()



    def __on_new_device_connected(self, device_socket, device_address, type) -> None:
        # if device is not already connected
        if not self.__is_device_in_list(device_address[0]):
            # init threading device
            device = DeviceObject(self.__kernel__, type, device_socket, device_address)
            # start threading device
            device.start()
            # add to listes
            self.__add_device_to_list(device)
            # add to db
            self.__add_device_to_db(device)

    def __bind_adress(self) -> None:
        try:
            # bind server address & port for device connection
            self._socket.bind((self._host, self._port))
            self.__console__.info("{} Listening port set on '{}'".format(self.__classname__, self._port))
        except:
            # get a random port if port already taken
            self.__console__.error("{} Port '{}' already used".format(self.__classname__, self._port))
            self._port = self.__random_port()
            self._socket.bind((self._host, self._port))
            self.__console__.info("{} Listening port set on '{}'".format(self.__classname__, self._port))

        # init ip
        ip = "{}:{}".format(self.__kernel__.server_private_ip, self._port)
        self.__console__.link("{} [IP] Address for Device connection : '{}'".format(self.__classname__, ip), link=ip)

        # set listen max device connected
        self._socket.listen(self._max_devices_authorized)
        self.__console__.info("{} {} devices max authorized".format(self.__classname__, self._max_devices_authorized))

    def __add_device_to_list(self, device: DeviceObject) -> None:
        # add to device list
        self.DEVICES_CONNECTED_LIST.append(device)

    def __add_device_to_db(self, device: DeviceObject) -> None:
        # insert or update in db
        self.__insert_or_update_in_db(device.get_name(), device.get_ip(), device.get_mac(), device.get_vendor())

    def __is_device_in_list(self, ip: str) -> bool:
        # itterate devices
        for device_in_list in self.DEVICES_CONNECTED_LIST:
            # if device ip is egal to an ip in list
            if ip == device_in_list.get_ip():
                # return True
                return True
        # return None
        return False

    def __is_device_in_db(self, target_ip: str) -> bool:
        # check if exist in db
        if self._database.get(self._db_table, what='ip', where="ip", where_value=target_ip):
            return True
        else:
            return False

    def __get_type_from_header(self, header: str) -> str:
        # get header
        header_type = header.split(":")[0]
        # get type
        type = header.split(":")[1]
        # if header typeis ok
        if header_type == "App-Type":
            # if type is ok
            if type == "controllable" or type == "requester":
                # return the type
                return type
            else:
                # else return None
                return None
        else:
            return None

    def __get_max_device_authorized(self) -> int:
        try:
            return int(self.__kernel__.BootFile.get_value("max_devices_authorized"))
        except:
            return 50

    def __insert_or_update_in_db(self, name: str, ip: str, mac: str, vendor: str) -> None:
        # check if exist in db by getting the ip
        if not self.__is_device_in_db(ip):
            # if not exist insert the device
            device_dict = {"ip": ip, "name": name, "alias": 'aucun', "mac": mac, "vendor": vendor}
            self._database.insert(self._db_table, device_dict)
        else:
            # else update in db
            self._database.update(self._db_table, "ip", ip, "ip", ip)
            self._database.update(self._db_table, "name", name, "ip", ip)
            self._database.update(self._db_table, "mac", mac, "ip", ip)
            self._database.update(self._db_table, "vendor", vendor, "ip", ip)

    def __accept_incoming_connection(self):
        try:
            # accept device and return socket & address
            device_socket, device_address = self._socket.accept()
        except socket.timeout:
            # if error return None
            device_socket, device_address = None, None
        return device_socket, device_address

    def __random_port(self) -> int:
        # get random int for port
        import random
        return int(random.randint(2000, 10000))

    def __stopping_handler(self) -> None:
        """ Close the client socket threads and server socket if they exists. """
        # disconnect every client
        for device in self.DEVICES_CONNECTED_LIST:
            device.disconnect()
            device._socket.join()
        # close device handler socket
        if self._socket:
            self._socket.close()
            self._socket = None

    def __stop_handling_devices(self) -> None:
        # stop the loop for accepting devices
        self._waiting_device_connection = False