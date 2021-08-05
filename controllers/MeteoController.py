import requests

from controllers.GeolocalisationController import GeolocalisationController
# ========================================== FIN DES IMPORTS ========================================================= #


class MeteoController:

    def __init__(self, geolocalisation: str):
        # init localisation
        self.__geolocalisation = geolocalisation
        # data json request
        self.__request_url = "https://api.openweathermap.org/data/2.5/weather?q={},fr&units=metric&appid=4025ff744d914dd5f05a3b9bd798f413&lang=fr".format(self.__geolocalisation)
        self.__request = requests.get(self.__request_url)
        self.request_data = self.__request.json()



    def temperature(self):
        try:
            return "{}°".format(str(int(self.request_data['main']['temp'])))
        except:
            return "Température inconnue"

    def weather(self):
        try:
            return str(self.request_data['weather'][0]['description'])
        except:
            return "Infos inconnue"

    def wind_speed(self):
        try:
            calcul = (int(self.request_data['wind']['speed']) * 3600) / 1000
            return "{} Km/h".format(str(int(calcul)))
        except:
            return "Infos inconnue"

    def url_img_weather(self):
        try:
            url = "http://openweathermap.org/img/wn/{}.png".format(str(self.request_data['weather'][0]['icon']))
            return url
        except:
            return None

    def get_request_data(self):
        return self.request_data
