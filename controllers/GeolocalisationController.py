import requests

from controllers.NetworkController import NetworkController
# ========================================== FIN DES IMPORTS ========================================================= #


class GeolocalisationController:


    @staticmethod
    def get_localisation():
        try:
            getData = requests.get('http://ip-api.com/json/' + NetworkController.public_ip())
            geolocalisation = getData.json()
            return str(geolocalisation['city'])
        except:
            return 'Ville non localisé'

    @staticmethod
    def get_pays():
        try:
            getData = requests.get('http://ip-api.com/json/' + NetworkController.public_ip())
            geolocalisation = getData.json()
            return str(geolocalisation['country'])
        except:
            return 'Pays non localisé'

    @staticmethod
    def get_region():
        try:
            getData = requests.get('http://ip-api.com/json/' + NetworkController.public_ip())
            geolocalisation = getData.json()
            return str(geolocalisation['regionName'])
        except:
            return 'Region non localisé'

    @staticmethod
    def get_cp():
        try:
            getData = requests.get('http://ip-api.com/json/' + NetworkController.public_ip())
            geolocalisation = getData.json()
            return str(geolocalisation['zip'])
        except:
            return 'Code postale non localisé'

