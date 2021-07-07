import os
import sys
# ========================================== FIN DES IMPORTS ========================================================= #


class FolderController:

    @staticmethod
    def create_folder(path: str):
        if not FolderController.if_folder_exist(path):
            try:
                # make folder
                os.mkdir(path)
                # making non-root perm folder
                if "linux" in sys.platform:
                    os.system('chmod u+x "' + str(path) + '"')
            except:
                raise Exception("Unable to create Folder '{}'".format(path))


    @staticmethod
    def remove_folder(path: str):
        if FolderController.if_folder_exist(path):
            try:
                # remove folder
                os.rmdir(path)
            except:
                raise Exception("Unable to remove Folder '{}'".format(path))


    @staticmethod
    def if_folder_exist(path: str, create_if_not_exist: bool=False):
        if os.path.exists(path):
            return True
        else:
            if create_if_not_exist:
                FolderController.create_folder(path)
                return True
            return False


    @staticmethod
    def is_dir(path: str):
        if os.path.isdir(path):
            return True
        else:
            return False