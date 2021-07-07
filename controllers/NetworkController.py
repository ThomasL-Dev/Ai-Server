from urllib.request import urlopen
import socket
from requests import get
# ========================================== FIN DES IMPORTS ========================================================= #


class NetworkController:


    @staticmethod
    def private_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        return local_ip


    @staticmethod
    def public_ip():
        try:
            ip = get('https://api.ipify.org').text
            return str(ip)
        except:
            return "0.0.0.0"


    @staticmethod
    def statut():
        try:
            urlopen('http://www.google.com', timeout=1)
            return "Connecté à internet"
        except:
            return "Déconnecté d'internet"


    @staticmethod
    def ip_info(ip: str):
        try:
            Data = get("http://ip-api.com/json/"+ip, verify=False)
            info = Data.json()

            if info['status'] == "fail":
                return "Pas d'informations"
            else:
                return "L'adresse ip se situe à " + info['city'] + " - " + info['country']
        except:
            return "Pas d'informations"

    @staticmethod
    def is_local_ip(ip: str):
        if "192.168." in str(ip) or str(ip) == "127.0.0.1" or str(ip) == "::1":
            return True
        return False