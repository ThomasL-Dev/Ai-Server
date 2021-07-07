import requests

from controllers.GeolocalisationController import GeolocalisationController
# ========================================== FIN DES IMPORTS ========================================================= #


class MeteoController:


    @staticmethod
    def temperature():
        try:
            weather_data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + GeolocalisationController.get_localisation() + ",fr&units=metric&appid=4025ff744d914dd5f05a3b9bd798f413&lang=fr")
            weather = weather_data.json()

            return str(int(weather['main']['temp'])) + "°"
        except:
            return "Température inconnue"


    @staticmethod
    def weather():
        try:
            weather_data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + GeolocalisationController.get_localisation() + ",fr&units=metric&appid=4025ff744d914dd5f05a3b9bd798f413&lang=fr")
            weather = weather_data.json()

            return str(weather['weather'][0]['description'])
        except:
            return "Infos inconnue"


    @staticmethod
    def wind_speed():
        try:
            weather_data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + GeolocalisationController.get_localisation() + ",fr&units=metric&appid=4025ff744d914dd5f05a3b9bd798f413&lang=fr")
            weather = weather_data.json()
            calcul = (int(weather['wind']['speed']) * 3600) / 1000
            return str(int(calcul)) + " Km/h"
        except:
            return "Infos inconnue"


    @staticmethod
    def url_img_weather():
        try:
            weather_data = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + GeolocalisationController.get_localisation() + ",fr&units=metric&appid=4025ff744d914dd5f05a3b9bd798f413&lang=fr")
            weather = weather_data.json()
            url = "http://openweathermap.org/img/wn/" + str(weather['weather'][0]['icon']) + ".png"
            return url
        except:
            return None


