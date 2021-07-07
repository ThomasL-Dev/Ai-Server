import discord
import logging
import asyncio

from binaries.builders.RequestBuilder import RequestBuilder
from binaries.obj.AiObject import AiObject

from controllers.TimeController import TimeController
from controllers.DateController import DateController

# setting logger lvl
_logger = logging.getLogger("discord")
_logger.setLevel(logging.CRITICAL)
_logger = logging.getLogger("asyncio")
_logger.setLevel(logging.CRITICAL)
# ========================================== FIN DES IMPORTS ========================================================= #


class DiscordObject(discord.Client, AiObject):

    def __init__(self, kernel):
        super(DiscordObject, self).__init__()
        AiObject.__init__(self, kernel)
        # init custom internal cmd
        self._INTERNAL_CMD = ['/get_skills', "/get_devices", "/cmds"]
        # init var for sending log from async loop
        self._LOG_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = False
        self._LOG_TEXT_FROM_OUTSIDE_ASYNC_LOOP = None
        self._LOG_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP = None
        # init var for sending chat text from async loop
        self._CHAT_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = False
        self._CHAT_TEXT_FROM_OUTSIDE_ASYNC_LOOP = None
        self._CHAT_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP = None



    async def on_ready(self):
        # change bot name with ai name
        await self.user.edit(username=self.__kernel__.ia_name)
        # change activity name
        await self.change_presence(activity=discord.Game(name="Version : {} | {}".format(self.__kernel__.get_version(), str(self._INTERNAL_CMD).replace("'", "").replace("[", "").replace("]", ""))))
        # create loop task to send msg
        self.loop.create_task(self.__task_for_outside_async_loop())



    async def on_message(self, message):
        if message.author != self.user:  # don't respond to ourselves
            # setting the channel where reponse is sent
            self._CHAT_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP = message.channel
            # text input from user
            user_input = str(message.content)
            # check if not an internal cmd
            if not self.__check_if_internal_cmd(user_input):
                # create request
                RequestBuilder(self.__kernel__, "Discord", user_input)

            else:
                # else is an internal cmd
                if user_input.startswith("/"):
                    # checks commandes
                    if "/cmds" == user_input:
                        await self.__cmd_get_cmds()
                    if "/get_skills" == user_input:
                        await self.__cmd_get_skills()
                    if "/get_devices" == user_input:
                        await self.__cmd_get_devices()



    def send_log_outside_from_async_loop(self, string: str=None, channel_id: int=None) -> None:
        if string is not None or channel_id is not None:
            self._LOG_TEXT_FROM_OUTSIDE_ASYNC_LOOP = string
            self._LOG_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP = channel_id
            self._LOG_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = True

    def send_chat_outside_from_async_loop(self, string: str=None) -> None:
        if string is not None:
            self._CHAT_TEXT_FROM_OUTSIDE_ASYNC_LOOP = string
            self._CHAT_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = True



    async def __cmd_get_cmds(self) -> None:
        # return the list of skills cmd
        if len(self.__kernel__.SkillHandler.SKILLS_LIST) < 1:
            await self.__send_chat("Aucun élément trouvé")
        else:
            out = ""
            out += ">>> [COMMANDES] \n\n"
            for skill in self.__kernel__.SkillHandler.SKILLS_LIST:
                out += "/" + str(skill.cmd) + "\n"
            await self.__send_chat(out)

    async def __cmd_get_skills(self) -> None:
        # return the list skill
        if len(self.__kernel__.SkillHandler.SKILLS_LIST) < 1:
            await self.__send_chat("Aucun élément trouvé")
        else:
            out = ""
            for skill in self.__kernel__.SkillHandler.SKILLS_LIST:
                out += str(skill) + "\n\n"
            await self.__send_chat(out)

    async def __cmd_get_devices(self) -> None:
        # return the device list
        if len(self.__kernel__.DevicesHandler.DEVICES_CONNECTED_LIST) < 1:
            await self.__send_chat("Aucun élément trouvé")
        else:
            out = ""
            for device in self.__kernel__.DEVICES_CONNECTED_LIST:
                out += str(device) + "\n\n"
            await self.__send_chat(out)



    async def __send_chat(self, string: str) -> None:
        # create string
        string = "```{}```".format(string)
        # send msg to specific channel
        await self._CHAT_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP.send(string)

    async def __send_log(self, string: str, channel_id: int) -> None:
        # create string
        string = "```[{} - {}] {}```".format(DateController.get_date(), TimeController.get_time(), string)
        # send msg to specific channel
        await self.get_channel(channel_id).send("{}".format(string))



    async def __task_for_outside_async_loop(self) -> None:
        while True:
            # if log channel flag is trigerred
            if self._LOG_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP:
                # send to log channel
                await self.__send_log(str(self._LOG_TEXT_FROM_OUTSIDE_ASYNC_LOOP), int(self._LOG_CHANNEL_FROM_OUTSIDE_ASYNC_LOOP))
                self._LOG_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = False

            # if chat channel flag is trigerred
            elif self._CHAT_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP:
                # send to chat channel
                await self.__send_chat(self._CHAT_TEXT_FROM_OUTSIDE_ASYNC_LOOP)
                self._CHAT_FLAG_SEND_TEXT_FROM_OUTSIDE_ASYNC_LOOP = False

            # wait a bit
            await asyncio.sleep(0.15)



    def __check_if_internal_cmd(self, string: str):
        # if the srting is in cmd list
        if string in self._INTERNAL_CMD:
            # return True
            return True
        # else return False
        return False