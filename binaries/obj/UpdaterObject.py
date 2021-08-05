import os
import urllib.request
import zipfile

from binaries.obj.AiObject import AiObject
from controllers.FileController import FileController
from controllers.FolderController import FolderController
# ========================================== FIN DES IMPORTS ========================================================= #


class UpdaterObject(AiObject):

    def __init__(self, kernel, dropbox_url_version_file: str, dropbox_url_binaries_zip: str):
        AiObject.__init__(self, kernel)
        # init file in zip
        self._zip_files_list = []
        # init urls to dl
        self._version_file_updated_url = dropbox_url_version_file
        self._zip_folder_updated_url = dropbox_url_binaries_zip
        # init versions file
        self._temp_version_updated_file = "version_updated.txt"
        # extract file to this folder
        self._extract_folder = os.path.join(os.path.split(os.getcwd())[0])
        # init temp zip file
        self._tmp_zip_file = "tmp.zip"

        # if version file do not exist
        if not FileController.if_file_exist(self.__kernel__.PATH_FILE_VERSION):
            # create it
            FileController.create_file(self.__kernel__.PATH_FILE_VERSION, "v0")



    def update(self) -> None:
        if not os.path.exists(os.path.join(self.__kernel__.PATH_FOLDER_CONFIG, "no_update.txt")):
            try:
                installed_version = self.get_installed_version()
                updated_version = self.get_updated_version()
                # diff between installed and updated version
                if self.check_if_new_update(installed_version, updated_version):
                    # update every files
                    self.__update_binaries_files()
                    # write new version in installed file
                    FileController.write_file(self.__kernel__.PATH_FILE_VERSION, updated_version)
                    self.__console__.kernel("{} Update finish".format(self.__classname__))
                    # restart program
                    self.__kernel__.restart()
                else:
                    self.__console__.info("{} Update not needed".format(self.__classname__))
            except Exception as e:
                self.__console__.error("{} Error while updating : {}".format(self.__classname__, e))
        else:
            self.__console__.kernel("{} Passing update".format(self.__classname__))

    def check_if_new_update(self, v1: str, v2: str) -> bool:
        if v1 != v2:
            return True
        else:
            return False


    def get_updated_version(self) -> str:
        try:
            # download the version file in dropbox
            self.__download_file(self._version_file_updated_url, self._temp_version_updated_file)
            # get version live
            version_up = FileController.read_file(self._temp_version_updated_file)[0]
            # remove the file
            FileController.remove_file(self._temp_version_updated_file)
            return str(version_up)
        except:
            return "0"

    def get_installed_version(self) -> str:
        try:
            # open version file already installed
            version = FileController.read_file(self.__kernel__.PATH_FILE_VERSION)[0]
            # return version txt
            return str(version)
        except:
            return "0"



    def __remove_void_folder(self) -> None:
        for dir, dirname, filenames in os.walk(os.getcwd()):
            # if there are no file in folder
            if len(filenames) == 0:
                try:
                    # remove folder
                    FolderController.remove_folder(dir)
                except:
                    pass

    def __remove_old_file(self) -> None:
        self.__console__.info("{} Removing previous file we do not longer need".format(self.__classname__))
        # check difference beetwen this 2 list
        diff = list(set(self._zip_files_list) ^ set(self.__get_files_extracted()))
        # itterate every difference
        for diff_path in diff:
            # remove useless file only
            if not str(diff_path).endswith("/") and self.get_installed_version() not in str(diff_path).lower() and "/." not in str(diff_path) and not str(diff_path).startswith(".") and "controllers/" not in str(diff_path).lower() and "skills/" not in str(diff_path).lower() and "routes/" not in str(diff_path).lower():
                try:
                    FileController.remove_file(os.path.join(self._extract_folder, diff_path))
                except:
                    pass

    def __get_files_extracted(self) -> list:
        # init list of file extracted
        out = []
        # itterate every file in given path
        for dir, dirname, filenames in os.walk(os.getcwd()):
            # for file in folder
            for filename in filenames:
                # add to list of file extracted
                out.append("{}{}".format(self._zip_files_list[0], os.path.join(dir, filename).replace("\\", "/").split(self._zip_files_list[0])[1]))
        return out

    def __update_binaries_files(self) -> None:
        self.__console__.kernel("{} Updating".format(self.__classname__))
        # dl zip file
        self.__download_file(self._zip_folder_updated_url, self._tmp_zip_file)
        # extract zip file
        self.__extract_temp_bin_zip_file()
        # remove zip file
        FileController.remove_file(self._tmp_zip_file)
        # remove previous file no longer needed
        self.__remove_old_file()
        # remove void folder
        self.__remove_void_folder()

    def __download_file(self, url: str, filename_output: str) -> None:
        try:
            # download file
            filename, __ = urllib.request.urlretrieve(url, filename=filename_output)
        except Exception as e:
            self.__console__.error("Error while downloading '{}' temp binaries files".format(filename_output, e))

    def __extract_temp_bin_zip_file(self) -> None:
        try:
            # open zip file
            with zipfile.ZipFile(self._tmp_zip_file, 'r') as zip_file:
                # extract every file in zip
                zip_file.extractall(self._extract_folder)
                # list every file in zip
                for filename in zip_file.namelist():
                    # add zip file to list
                    self._zip_files_list.append(filename)
                zip_file.close()
        except Exception as e:
            self.__console__.error("Error while exctracting files from '{}' temp binaries files : {}".format(self._tmp_zip_file, e))


