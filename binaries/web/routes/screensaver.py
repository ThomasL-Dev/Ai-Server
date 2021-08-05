from binaries.web.obj.BasePage import BasePage

from controllers.NetworkController import NetworkController
from controllers.DateController import DateController
from controllers.MeteoController import MeteoController
from controllers.GeolocalisationController import GeolocalisationController
# ========================================== FIN DES IMPORTS ========================================================= #



class screensaver(BasePage):


    def on_get(self):
        # localisation
        if not NetworkController.is_local_ip(self.ip_requester): localisation = GeolocalisationController(self.ip_requester).get_localisation()
        else: localisation = GeolocalisationController(self.kernel.server_public_ip).get_localisation()
        # meteo
        meteo_controller = MeteoController(localisation)
        weather = meteo_controller.weather()
        degree = meteo_controller.temperature()
        wind_speed = meteo_controller.wind_speed()
        weather_img = meteo_controller.url_img_weather()

        self.render("screensaver.html",
                    ia_name=self.kernel.ia_name,

                    date=DateController.day_string() + " " + DateController.day_int(),
                    month=DateController.month_string(),
                    year=DateController.year(),

                    weather=weather,
                    degree=degree,
                    wind_speed=wind_speed,
                    weather_img=weather_img,

                    localisation=localisation,
                    )

