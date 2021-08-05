import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from pylgtv import WebOsClient  # pip3 install pylgtv

from pywebostv.connection import *
from pywebostv.controls import *  # pip3 install pywebostv
# ========================================== FIN DES IMPORTS ========================================================= #





class LgWebOsController:

    def __init__(self, ip: str):
        self._ip = ip
        self._key = None
        self._sound_lvl_before_mute = 10
        self._webos = None
        self._webos_controller = None

        self._connect_tv()
        self._connect_controller()

        if self.getStatut() is None:
            raise Exception('Cannot connect to LgWebOs')


    def getStatut(self):
        try:
            curent_app = self._webos.get_current_app()
            audio = self._webos.get_audio_status()['volume']
            return curent_app, audio
        except:
            return None


    def mute(self):
        self._sound_lvl_before_mute = self.get_sound_lvl()
        self._webos.set_volume(0)

    def unmute(self):
        if self.get_sound_lvl() == 0:
            self._webos.set_volume(int(self._sound_lvl_before_mute))

    def shutdown(self):
        self._webos.power_off()

    def popup(self, string=""):
        if string != "":
            self._webos.send_message(str(string))

    def get_apps(self):
        apps = {}
        for app in self._webos.get_apps():
            apps[app['title']] = [app['id'], app['largeIcon']]
        return apps

    def launch_app(self, app_name):
        apps = self.get_apps()
        for app in apps:
            if app_name in str(app).lower() or app_name in str(app).lower().replace(" ", ""):
                app_id = apps[app][0]
                self._webos.launch_app(app_id)


    def get_sound_lvl(self):
        return self._webos.get_volume()

    def volume_up(self):
        self._webos.volume_up()

    def volume_down(self):
        self._webos.volume_down()

    def set_volume(self, vol):
        self._webos.set_volume(int(vol))

    def channel_up(self):
        self._webos.channel_up()

    def channel_down(self):
        self._webos.channel_down()

    def key_home(self):
        self._webos_controller.connect_input()
        self._webos_controller.home()
        self._webos_controller.disconnect_input()

    def key_back(self):
        self._webos_controller.connect_input()
        self._webos_controller.back()
        self._webos_controller.disconnect_input()

    def key_ok(self):
        self._webos_controller.connect_input()
        self._webos_controller.ok()
        self._webos_controller.disconnect_input()

    def key_up(self):
        self._webos_controller.connect_input()
        self._webos_controller.up()
        self._webos_controller.disconnect_input()

    def key_down(self):
        self._webos_controller.connect_input()
        self._webos_controller.down()
        self._webos_controller.disconnect_input()

    def key_left(self):
        self._webos_controller.connect_input()
        self._webos_controller.left()
        self._webos_controller.disconnect_input()

    def key_right(self):
        self._webos_controller.connect_input()
        self._webos_controller.right()
        self._webos_controller.disconnect_input()




    def _connect_tv(self):
        try:
            self._webos = WebOsClient(self._ip)
            self._key = self._webos.client_key
        except Exception as e:
            raise Exception('Cannot connect to LgWebOs')


    def _connect_controller(self):
        try:
            self.tv_control = WebOSClient(self._ip)
            self.tv_control.connect()
            for status in self.tv_control.register({'client_key': self._key}):
                if status == WebOSClient.PROMPTED:
                    return
                elif status == WebOSClient.REGISTERED:
                    pass
            self._webos_controller = InputControl(self.tv_control)
        except Exception as e:
            raise Exception('LgWebOs controller not init')



