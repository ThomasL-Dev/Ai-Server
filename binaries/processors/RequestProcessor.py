from binaries.processors.SkillProcessor import SkillProcessor
from binaries.processors.NaturalLanguageProcessor import NaturalLanguageProcessor
from binaries.obj.RequestObject import RequestObject
from binaries.obj.SkillObject import SkillObject
from binaries.obj.AiObject import AiObject
# ========================================== FIN DES IMPORTS ========================================================= #



class RequestProcessor(AiObject):


    def __init__(self, kernel, request: RequestObject):
        AiObject.__init__(self, kernel)

        # init request info
        self.req_name = str(request.name)
        self.req_intent = str(request.input).replace("  ", " ")
        self.req_type = str(request.type)
        self.req_sender = str(request.sender)
        self.req_timestamp = str(request.timestamp)

        # init NLP
        self.nlp = NaturalLanguageProcessor(input=self.req_intent)

        # init temp vars
        if self.req_type == "text":
            self.__temp_utterance_found = None
        elif self.req_type == "cmd":
            self.__temp_cmd = self.__extract_cmd()
            self.__temp_ip = None
            self.__temp_param = None



    def start(self):
        try:
            # processing request
            self.__console__.info("{} Processing '{}' : '{}'".format(self.__classname__, self.req_name, self.req_intent))
            self.on_processing()
            # resetting temp ars
            self.__reset_temp_vars()
        except Exception as e:
            self.__console__.error('{} Error while processing request : {}'.format(self.__classname__, e))

    def on_processing(self):
        # search skill
        skill = self.__search_skill()
        # if skill is not None
        if skill is not None:
            # getting ip if needed
            ip_to_process = self.__get_ip_to_process(skill)
            # getting param if needed
            param_to_process = self.__get_param_to_process(skill)
            # launch the skill processor
            SkillProcessor(self.__kernel__, skill, self.req_sender).process(ip=ip_to_process, param=param_to_process)

        else:
            self.__console__.error("{} No Skill found for request '{}'".format(self.__classname__, self.req_name))



    def __get_ip_to_process(self, skill) -> str:
        # if skill need to find a device in list
        if skill.find_device_in_list:
            self.__console__.info("{} Getting ip for skill '{}'".format(self.__classname__, skill))
            # if request type is text
            if self.req_type == "text":
                """ si la requete est du texte """
                # search & return ip found by nlp
                return self.__search_ip_by_nlp()
            # if request type is cmd
            elif self.req_type == "cmd":
                """ si la requete est une commande """
                # search & return ip found by cmd
                return self.__search_ip_by_command()
            else:
                return None
        else:
            return None

    def __get_param_to_process(self, skill) -> str:
        # if skill need a param
        if skill.need_param:
            self.__console__.info("{} Getting param for skill '{}'".format(self.__classname__, skill))
            # if request type is text
            if self.req_type == "text":
                """ si la requete est du texte """
                # search & return param found by nlp
                return self.__search_param_by_nlp()
            # if request type is cmd
            elif self.req_type == "cmd":
                """ si la requete est une commande """
                # search & return param found by cmd
                return self.__search_param_by_command()

            else:
                return None
        else:
            return None

    def __search_skill(self) -> SkillObject:
        self.__console__.info("{} Searching Skill ...".format(self.__classname__))
        # itterate skills
        for skill_in_list in self.__kernel__.SkillHandler.SKILLS_LIST:
            # if request type is text
            if self.req_type == "text":
                """ si la requete est du texte """
                # search & return skill found by nlp
                skill_found = self.__search_skill_by_nlp(skill_in_list)
            # if request type is cmd
            elif self.req_type == "cmd":
                """ si la requete est une commande """
                # search & return skill found by nlp
                skill_found = self.__search_skill_by_command(skill_in_list)
            else:
                break  # sinon on arrete (aucun type de requete reconnu)

            if skill_found is not None:
                # return skill
                return skill_found

        return None

    def __search_skill_by_nlp(self, skill_in_list) -> SkillObject:
        # itterate utterance
        for utterance in skill_in_list.utterance:
            # find equality by nl
            equality = self.nlp.find_equality(pattern=utterance)
            # set temp utterance var
            self.__temp_utterance_found = utterance
            # if equality
            if equality:
                # return skill
                return skill_in_list
        # else return None
        return None

    def __search_ip_by_nlp(self) -> str:
        # itterate device
        for device in self.__kernel__.DevicesHandler.DEVICES_CONNECTED_LIST:
            # if name in request intent
            if device.get_name().lower() in self.req_intent.lower():
                # if device ip is not None
                if device.get_ip() is not None:
                    # return device ip
                    return device.get_ip()
            # else alias in request intent
            elif device.get_alias().lower() in self.req_intent.lower():
                # if device ip is not None
                if device.get_ip() is not None:
                    # return device ip
                    return device.get_ip()
        return None

    def __search_param_by_nlp(self) -> str:
        # return param if found by nlp
        return self.nlp.extract_slot(pattern=self.__temp_utterance_found)

    def __search_skill_by_command(self, skill_in_list) -> object:
        # if skill cmd is egal to temp cmd
        if skill_in_list.cmd == self.__temp_cmd:
            # return the skill
            return skill_in_list
        # else return None
        return None

    def __search_param_by_command(self) -> str:
        # get and init temp intent
        tmp_intent = self.req_intent.split(" ")
        # init param
        param = ""

        # remove cmd from intent
        tmp_intent.remove("/" + self.__temp_cmd)

        # remove ip from intent
        if self.__temp_ip is not None:
            tmp_intent.remove(self.__temp_ip)

        # reconstruct the param
        for word in tmp_intent:
            param += word + " "

        if int(len(param)) > 1:  # if returned intent is not null
            return param[:-1]  # [:-1] remove the last space added
        else:
            return None

    def __search_ip_by_command(self) -> str:
        # itterate word in intent
        for word in self.req_intent.split(" "):
            # if there is 3 point like 0.0.0.0
            if word.count(".") == 3:
                # set temp ip with the word
                self.__temp_ip = word
                # return word
                return word
        # else return None
        return None

    def __reset_temp_vars(self) -> None:
        # resetting every temp vars
        if self.req_type == "text":
            self.__temp_utterance_found = None

        elif self.req_type == "cmd":
            self.__temp_cmd = None
            self.__temp_ip = None
            self.__temp_param = None

    def __extract_cmd(self) -> str:
        # return the first word when type request is cmd
        return self.req_intent.split(" ")[0].replace("/", "")
