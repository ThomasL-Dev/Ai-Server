import os
import sys
# ========================================== FIN DES IMPORTS ========================================================= #


class FileController:


    @staticmethod
    def create_file(path: str, data: str=None):
        if not FileController.if_file_exist(path):
            try:
                # create file
                with open(path, "w+") as file:
                    # write data  when file is created if needed
                    if data is not None:
                        file.write(data)
                    # close the file
                    file.close()
                # making non-root perm folder
                if "linux" in sys.platform:
                    os.system('chmod u+x "' + str(path) + '"')
            except:
                raise Exception("Unable to create File '{}'".format(path))

    @staticmethod
    def remove_file(path: str):
        if FileController.if_file_exist(path):
            try:
                os.remove(path)
            except:
                raise Exception("Unable to remove File '{}'".format(path))


    @staticmethod
    def remove_all_file_in_folder(path: str):
        for file in os.listdir(path):
            FileController.remove_file(os.path.join(path, file))


    @staticmethod
    def if_file_exist(path: str, create_if_not_exist: bool=False):
        if os.path.exists(path):
            return True
        else:
            if create_if_not_exist:
                FileController.create_file(path)
                return True
            return False


    @staticmethod
    def is_file(path: str):
        if os.path.isfile(path):
            return True
        else:
            return False


    @staticmethod
    def write_file(path: str, data: str):
        if FileController.if_file_exist(path):
            with open(path, "w+") as file:
                file.write(data)
                file.close()
        else:
            FileController.create_file(path, data)


    @staticmethod
    def read_file(path: str):
        if FileController.if_file_exist(path):
            with open(path, "r+") as file:
                data = file.readlines()
                file.close()
            return data
        else:
            raise Exception("File '{}' do not exist".format(path))