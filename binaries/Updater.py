import os
import urllib.request
import zipfile
import sys
import time


class Updater:

    def __init__(self):
        # url version file
        self._version_file_url = "https://www.dropbox.com/s/jtgs1k6z23fm44c/server_version.txt?dl=1"
        # init version file
        self._version_installed_file = "version.txt"
        self._version_live_file = "live_version.txt"
        # init temp zip file
        self._tmp_zip_file = "tmp.zip"
        # url for dl the file
        self._url_zip = "https://www.dropbox.com/s/5ggzgp8rjacea1b/Server.zip?dl=1"
        # extract file to this folder
        self._extract_folder = os.path.join(os.path.split(os.getcwd())[0])  # ".." to replace all file directly no need to copy etc

        # init version var
        self._live_version = None
        self._installed_version = None



    def start(self):
        if not os.path.exists(os.path.join(".cfg", "no_update.txt")):
            try:
                # on check & get version from live and installed file
                self.__check_installed_version()
                self.__check_live_version()

                if self._installed_version != self._live_version:
                    print("Starting to update")
                    # dl zip file
                    self.__download_file(self._url_zip, self._tmp_zip_file)
                    # extart zip file
                    self.__extract_zip_file(self._tmp_zip_file)
                    # remove zip file
                    self.__remove_file(self._tmp_zip_file)
                    # write new version in installed file
                    self.__write_version_installed_file()
                    print("Update finish")
                    print("Restarting...")
                    time.sleep(2)
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
                else:
                    print("No need to update")
            except:
                print("Error while doing update")



    def __download_file(self, url: str, filename_output: str):
        try:
            # download file
            filename, __ = urllib.request.urlretrieve(url, filename=filename_output)
            print("File '" + str(filename) + "' downloaded")
        except:
            print("Error while downloading '" + str(self._tmp_zip_file) + "' file")

    def __extract_zip_file(self, file_name: str):
        print("Extracting '" + file_name + "' folder")
        try:
            # open zip file
            with zipfile.ZipFile(file_name, 'r') as zip_file:
                # extract every file in zip
                zip_file.extractall(self._extract_folder)
                zip_file.close()
                print("'" + file_name + "' file Extracted")
        except Exception as e:
            print("Error while extracting '" + str(file_name) + "' folder")

    def __remove_file(self, file_name: str):
        try:
            # remove file
            os.remove(file_name)
            print("File '" + file_name + "' removed")
        except:
            print("Error while removing '" + file_name + "' file")

    def __check_installed_version(self):
        # check already installed version
        if not os.path.exists(self._version_installed_file):
            # create version file
            self.__create_version_installed_file()
        else:
            # get installed version
            self._installed_version = self.__read_version_file(self._version_installed_file)

    def __check_live_version(self):
        # check the live version
        # download the version file in dropbox
        self.__download_file(self._version_file_url, self._version_live_file)
        # get version live
        self._live_version = self.__read_version_file(self._version_live_file)
        # remove the file
        self.__remove_file(self._version_live_file)

    def __read_version_file(self, file_name: str):
        # read file
        with open(file_name, "r+") as v_file:
            # get version
            version = v_file.readline()
            v_file.close()
        return version

    def __write_version_installed_file(self):
        # write the version in version file
        with open(self._version_installed_file, "w+") as f:
            f.write(self._live_version)
            f.close()

    def __create_version_installed_file(self):
        # create version file
        with open(self._version_installed_file, "w+") as f:
            f.write("0")
            self._installed_version = "0"
            f.close()
