import requests

from controllers.NetworkController import NetworkController
# ========================================== FIN DES IMPORTS ========================================================= #


class GeolocalisationController:

    def __init__(self, ip: str):
        # init ip
        self.__ip = ip
        # data json request
        self.__request_url = 'http://ip-api.com/json/{}'.format(self.__ip)
        self.__request = requests.get(self.__request_url)
        self.request_data = self.__request.json()



    def get_localisation(self):
        try:
            return str(self.request_data['city'])
        except:
            return 'Ville non localisé'

    def get_pays(self):
        try:
            return str(self.request_data['country'])
        except:
            return 'Pays non localisé'

    def get_region(self):
        try:
            return str(self.request_data['regionName'])
        except:
            return 'Region non localisé'

    def get_cp(self):
        try:
            return str(self.request_data['zip'])
        except:
            return 'Code postale non localisé'

    def get_request_data(self):
        return self.request_data