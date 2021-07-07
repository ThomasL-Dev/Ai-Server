import time
# ========================================== FIN DES IMPORTS ========================================================= #

class TimeController:

    @staticmethod
    def heure():
        return time.strftime('%H', time.localtime())

    @staticmethod
    def minute():
        return time.strftime('%M', time.localtime())

    @staticmethod
    def seconde():
        return time.strftime('%S', time.localtime())

    @staticmethod
    def get_time():
        return time.strftime('%H:%M:%S', time.localtime())