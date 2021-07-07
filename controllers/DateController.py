import time
# ========================================== FIN DES IMPORTS ========================================================= #

class DateController:

    @staticmethod
    def day_int():
        return time.strftime('%d', time.localtime())

    @staticmethod
    def day_string():
        return time.strftime('%A', time.localtime()).replace("Monday", "Lundi").replace("Tuesday", "Mardi").replace("Wednesday", "Mercredi").replace("Thursday", "Jeudi").replace("Friday", "Vendredi").replace("Saturday", "Samedi").replace("Sunday", "Dimanche")

    @staticmethod
    def mont_int():
        return time.strftime('%m', time.localtime())

    @staticmethod
    def month_string():
        return time.strftime('%B', time.localtime()).replace("January", "Janvier").replace("February", "Février").replace("March", "Mars").replace("April", "Avril").replace("May", "Mai").replace("June", "Juin").replace("July", "Juillet").replace("August", "Aout").replace("September", "Septembre").replace("October", "Octobre").replace("November", "Novembre").replace("December", "Décembre")

    @staticmethod
    def year():
        return time.strftime('%Y', time.localtime())

    @staticmethod
    def get_date():
        return time.strftime('%d/%m/%Y', time.localtime())
