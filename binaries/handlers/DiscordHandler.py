import asyncio

from binaries.obj.AiObject import AiObject
from binaries.obj.HandlerObject import HandlerObject
from binaries.obj.DiscordObject import DiscordObject
# ========================================== FIN DES IMPORTS ========================================================= #


class DiscordHandler(HandlerObject, AiObject):

    def __init__(self, kernel, token=None):
        HandlerObject.__init__(self, kernel)
        # init token
        self._token = token
        # init discord
        self._discord = None
        # init loop
        self.loop = asyncio.get_event_loop()



    def on_handling(self):
        self.loop.create_task(self.__start_discord())
        self.loop.run_forever()



    def send_chat(self, string: str) -> None:
        self._discord.send_chat_outside_from_async_loop(string)

    def send_log(self, string: str, channel_id: int) -> None:
        self._discord.send_log_outside_from_async_loop(string, channel_id)



    async def __start_discord(self) -> None:
        # init discord object
        self._discord = DiscordObject(self.__kernel__)
        try:
            # if token is not None
            if self._token is not None:
                # start the discord object
                await self._discord.start(self._token)
            else:
                # else raise error
                raise Exception("{} No Token found".format(self.__classname__))
        except Exception as e:
            self.__console__.error("{} Error : ".format(self.__classname__) + str(e))

