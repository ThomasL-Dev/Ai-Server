import random

from binaries.obj.AiObject import AiObject
from binaries.obj.VoiceObject import VoiceObject

from controllers.NetworkController import NetworkController
# ========================================== FIN DES IMPORTS ========================================================= #


class ReponseBuilder(AiObject):

    def __init__(self, kernel, sender, reponse):
        AiObject.__init__(self, kernel)

        # init var needed for reponse
        self._sender = sender
        self._reponse = reponse
        # create reponse
        self.__create_reponse()



    def __create_reponse(self):
        # find & init reponse
        reponse = self.__get_reponse()
        # if reponse is not None
        if reponse is not None:
            # if sender is discord
            if self._sender.lower() == "discord":
                # on lenvoi sur discord
                self.__kernel__.DiscordHandler.send_chat(reponse)
            else:
                # else speak reponse or send to a device
                self.__process_reponse(reponse)




    def __process_reponse(self, reponse: str):
        # get device
        device = self.__kernel__.DevicesHandler.get_device(self._sender, by="name")
        # if device is not None
        if device is not None:
            # if its a local request
            if NetworkController.is_local_ip(device.get_ip()):
                # ai speak
                VoiceObject(self.__kernel__).speak(reponse)
            else:
                # else get device socket and send to the device
                device.get_socket().send(reponse)

    def __get_reponse(self):
        # if reponse type is a list
        if type(self._reponse) == list:
            # if there is at least 1 reponse
            if len(self._reponse) >= 1:
                # return random reponse
                return random.choice(self._reponse)
        else:
            # else return the string reponse
            return str(self._reponse)

