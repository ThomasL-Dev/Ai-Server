import configparser

from controllers.FileController import FileController
# ========================================== FIN DES IMPORTS ========================================================= #

class BootFile:

    def __init__(self, file_path=None):
        # init file path
        self._file_path = file_path
        # init class for read .ini files
        self._config = configparser.ConfigParser()
        # check if file exist
        if not FileController.if_file_exist(self._file_path):
            # if not exist create file with base infos
            self._create_base_file()



    def __repr__(self):
        # representation of the class
        output = f'{self.__class__.__name__}('

        sections = self._get_all_sections_and_options()
        for section in sections:
            output += f'{section}, '

        output += f')'
        output = output.replace(", )", ")")
        return output


    def update_value(self, option_name: str, new_value: str):
        # read the file
        self._read_boot_file()
        # get section
        section = self.get_section_by_option_name(option_name)
        # if section is not null
        if section is not None:
            # itterate every option in the section
            for option in section.options:
                # if option is egal to the name of option
                if option_name == option['name']:
                    # update the value
                    self._config[str(section.name)][option['name']] = new_value
                    # write in file if found
                    self._write_in_file()


    def get_value(self, option_name: str):
        # read the file
        self._read_boot_file()
        # get section
        sections = self._get_all_sections_and_options()
        # itterate sections
        for section in sections:
            # itterate option in section
            for option in section.options:
                # if the option enter is egal to option name
                if option_name == option['name']:
                    # return the option
                    return option['value']
        # else return none string
        return None


    def get_sections(self):
        # read the file
        self._read_boot_file()
        # get every sections
        return self._get_all_sections_and_options()


    def get_section_by_option_name(self, option_name: str):
        # read the file
        self._read_boot_file()
        # get every sections
        sections = self._get_all_sections_and_options()
        # itterate sections
        for section in sections:
            # if the option enter is egal to option name
            for option in section.options:
                # if the option enter is egal to option name
                if option_name == option['name']:
                    # return the section
                    return section
        # else return None
        return None


    def _create_base_file(self):
        # read the file
        self._config.read(self._file_path)
        # init sections and options
        self._config['PROPERTIES'] = {
            'ai_name': 'ai',
            'server_port': '33000',
            'max_devices_authorized': "50"
        }
        self._config['DISCORD'] = {
            'discord_token': "",
            'discord_channel_log_device': "",
            'discord_channel_log_account': "",
            'discord_channel_log_request': "",
        }
        self._config['DEBUG'] = {
            "disable_update": "false",
            "pass_install_requierements": "false",
        }
        # wrtie in file
        self._write_in_file()


    def _get_all_sections_and_options(self):
        # init a list
        output = []
        # read the file
        self._read_boot_file()
        # get every sections
        sections = self._config.sections()
        # itterate sections
        for section in sections:
            # get every options in section
            options = self._get_options_in_section(section)
            # create a new section object
            new_section = self.Section(section_name=section)
            # if the section object is not null and not alread in output list
            if new_section is not None and new_section.name not in output:
                try:
                    # itterate options
                    for option in options:
                        # name of the option
                        option_name = option[0]
                        # value of the options
                        option_value = option[1]
                        # add option to section object
                        new_section.add_new_option(option_name, option_value)
                    # add section to output list
                    output.append(new_section)
                except:
                    pass
        # return the list
        return output

    def _get_options_in_section(self, section_name: str):
        try:
            # read the file
            self._config.read(self._file_path)
            # get every options in section
            return self._config.items(section_name)
        except:
            pass


    def _read_boot_file(self):
        try:
            # read the .ini file
            self._config.read(self._file_path)
        except:
            pass

    def _write_in_file(self):
        # write in .ini file
        with open(self._file_path, "w+") as cfg_file:
            self._config.write(cfg_file)
            cfg_file.close()


    class Section:

        def __init__(self, section_name: str):
            # init sections name
            self.name = section_name
            # init list of options
            self.options = []

        def set_name(self, s: str):
            # set the name of section
            self.name = s

        def add_new_option(self, name: str, value: str):
            # create option data and add to list
            self.options.append({"name": name, "value": value})

        def __repr__(self):
            # represantation of the class
            output = f'{self.name}('

            for option in self.options:
                output += f'{option["name"]}={option["value"]}, '

            output += f')'
            output = output.replace(", )", ")")
            return output
