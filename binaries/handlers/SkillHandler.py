import sys
import os
import inspect
import time

from binaries.obj.AiObject import AiObject
from binaries.obj.SkillObject import SkillObject
from binaries.obj.HandlerObject import HandlerObject

from controllers.FileController import FileController
# ========================================== FIN DES IMPORTS ========================================================= #



class SkillHandler(HandlerObject, AiObject):


    def __init__(self, kernel, skill_path):
        HandlerObject.__init__(self, kernel)

        # init skills list
        self.SKILLS_LIST = []

        # skill folder path
        self._skills_folder_path = skill_path
        # fix the path
        self._skills_folder_path = self.__fix_skills_folder()
        # Add path to the system path
        self.__add_skill_folder_to_system_path(self._skills_folder_path)

        # loading skills at startup
        self.__console__.info("{} Loading Skills".format(self.__classname__))
        self.__load_skill_at_startup()



    def on_handling(self):
        # loop always running
        while True:
            # checking skills if removed or added
            self.__check_skills()
            time.sleep(0.7)



    def get_skill_by_name(self, skill_name: str) -> SkillObject:
        self.__console__.info("{} Getting skill '{}' object".format(self.__classname__, skill_name))
        # itterate skills
        for skill_in_list in self.SKILLS_LIST:
            # if skill is egal to skill name enter
            if skill_name in skill_in_list._name:
                # return the skill
                self.__console__.info("{} Skill '{}' object getted".format(self.__classname__, skill_name))
                return skill_in_list
        # else return None
        self.__console__.error("{} Skill '{}' object not found".format(self.__classname__, skill_name))
        return None


    def create_skill(self) -> None:
        # create skill file
        # load class in file
        # add skill to list
        # self.__add_skill_to_list()
        pass

    def remove_skill(self, skill_name: str) -> None:
        FileController.remove_file(os.path.join(self._skills_folder_path, skill_name + ".py"))



    def __check_skills(self) -> None:
        # get skills in folder
        skill_in_folder = self.__get_skills_in_folder()
        # if number of skill in folder is superior to skill in list
        if len(skill_in_folder) > len(self.SKILLS_LIST):
            self.__get_skill_added()
        # if number of skill in folder is inferior to skill in list
        elif len(skill_in_folder) < len(self.SKILLS_LIST):
            self.__get_skill_removed()
        else:
            pass

    def __get_skill_added(self) -> None:
        # check difference before and after skill list
        added = list(set(self.__get_skills_name_in_list()) ^ set(self.__get_skills_in_folder()))
        # itterate skill added
        for skill_added in added:
            # load skill by file
            self.__load_file_skill(skill_added)

    def __get_skill_removed(self) -> None:
        # check difference before and after skill list
        removed = list(set(self.__get_skills_in_folder()) ^ set(self.__get_skills_name_in_list()))
        # itterate skill removed
        for skill_removed in removed:
            # get skill object
            removed_obj = self.get_skill_by_name(skill_removed)
            # if not None
            if removed_obj is not None:
                # remove from list
                self.__remove_skill_from_list(removed_obj)

    def __add_skill_to_list(self, skill: SkillObject) -> None:
        # if skill not already exist
        if not self.__is_skill_in_list(skill._name):
            # add the skill to list
            self.SKILLS_LIST.append(skill)
            self.__console__.kernel("{} Skill '{}' added to list".format(self.__classname__, skill._name))

    def __remove_skill_from_list(self, skill: SkillObject) -> None:
        # if skill not already exist
        if self.__is_skill_in_list(skill._name):
            # add the skill to list
            self.SKILLS_LIST.remove(skill)
            self.__console__.kernel("{} Skill '{}' removed from list".format(self.__classname__, skill._name))

    def __load_file_skill(self, skill_file_name: str) -> None:
        # load skill class
        skill = self.__load_class_in_file(skill_file_name)
        # if skill is not null
        if skill is not None:
            # add the skill to list
            self.__add_skill_to_list(skill)

    def __get_skills_name_in_list(self) -> list:
        output = []
        for skill_in_list in self.SKILLS_LIST:
            output.append(skill_in_list._name)
        return output

    def __get_skills_in_folder(self) -> list:
        output = []
        # Load all the files in path
        for f in os.listdir(self._skills_folder_path):
            # Ignore anything that isn't a .py file and file name start by "Skill"
            if len(f) > 3 and f[-3:] == '.py' and "Skill" in f:
                # skill filename withtout the extension
                skill_file_name = f[:-3]
                # if skill is not already in skill list
                if skill_file_name not in self.SKILLS_LIST:
                    # add skill to output
                    output.append(skill_file_name)
        return output

    def __get_skill_file_infos(self, skill_file_name: str):
        # skill class path
        skill_class_path = skill_file_name.split('.')
        # module name
        module_class_name = '.'.join(skill_class_path[:-1])
        # class name
        class_name = skill_class_path[-1]
        return skill_class_path, module_class_name, class_name

    def __get_class_name(self, skill_file_name: str) -> str:
        # format skill class
        if "." not in skill_file_name:
            return skill_file_name + "." + skill_file_name
        else:
            return skill_file_name

    def __is_skill_in_list(self, skill_name: str) -> bool:
        # itterate skills
        for skill_in_list in self.SKILLS_LIST:
            # if skill enter is egal to an skill in list
            if skill_name in skill_in_list._name:
                # return True
                return True
        # else return False
        return False

    def __load_class_in_file(self, skill_file_name: str):
        try:
            # get the class in skill file
            skill_file_name = self.__get_class_name(skill_file_name)
            # check if all good in skill file
            skill_class_path, module_class_name, class_name = self.__get_skill_file_infos(skill_file_name)
            # Import the module
            __import__(module_class_name, globals(), locals(), ['*'])
            # Get the class
            _class = getattr(sys.modules[module_class_name], class_name)
            # Check if its a class
            if inspect.isclass(_class):
                # Return class
                return _class(self.__kernel__)
            else:
                # else return None
                return None
        except AttributeError as e:
            self.__console__.error("{} Skill class have not the same name as '{}' file name".format(self.__classname__, skill_file_name.split(".")[0]))
            return None

        except Exception as e:
            self.__console__.error("{} Error while loading skill '{}' : {}".format(self.__classname__, skill_file_name.split(".")[0], e))
            return None

    def __load_skill_at_startup(self) -> None:
        # itterate skills in folder skilsl path
        for skill_file_name in self.__get_skills_in_folder():
            # load skill
            self.__load_file_skill(skill_file_name)

    def __fix_skills_folder(self) -> str:
        # fix the path
        if self._skills_folder_path[-1:] != '/':
            self._skills_folder_path += '/'
        return self._skills_folder_path

    def __add_skill_folder_to_system_path(self, path: str) -> None:
        # Add path to the system path
        sys.path.append(path)

