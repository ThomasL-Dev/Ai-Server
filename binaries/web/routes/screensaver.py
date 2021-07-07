from binaries.web.obj.BasePage import BasePage

from controllers.DateController import DateController
from controllers.MeteoController import MeteoController
from controllers.GeolocalisationController import GeolocalisationController
# ========================================== FIN DES IMPORTS ========================================================= #



class screensaver(BasePage):


    def on_get(self):
        weather = MeteoController.weather()
        localisation = GeolocalisationController.get_localisation()
        degree = MeteoController.temperature()
        wind_speed = MeteoController.wind_speed()
        weather_img = MeteoController.url_img_weather()

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

