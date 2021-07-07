import os
import json

from binaries.obj.AiObject import AiObject
from binaries.obj.HandlerObject import HandlerObject
from binaries.obj.CameraObject import CameraObject
from controllers.FolderController import FolderController

from controllers.FileController import FileController
# ========================================== FIN DES IMPORTS ========================================================= #


class CamerasHandler(HandlerObject, AiObject):

    def __init__(self, kernel):
        HandlerObject.__init__(self, kernel)

        # init cams list
        self.CAMERAS_LIST = []

        # init folder where store things
        self._cameras_feed_folder = os.path.join(self.__kernel__.PATH_FOLDER_KERNEL, "binaries", "web", "static", "cameras")
        self._cameras_setting_folder = os.path.join(self.__kernel__.PATH_FOLDER_CONFIG, "cameras")
        # creating folder if they doesnt exist
        FolderController.create_folder(self._cameras_feed_folder)
        FolderController.create_folder(self._cameras_setting_folder)
        # init cams count
        self._camera_count = 0
        # loading all cameras stored when server start
        self.__load_all_cameras()



    def get_camera_count(self) -> str:
        # return number of cameras
        self.__console__.info("{} Getting camera count".format(self.__classname__))
        return str(self._camera_count)

    def get_camera_by_name(self, name: str) -> CameraObject:
        # itters every cams
        self.__console__.info("{} Getting camera '{}' object".format(self.__classname__, name))
        for camera_in_list in self.CAMERAS_LIST:
            # if name is egal to name enter
            if name in camera_in_list.get_name() or name in camera_in_list.get_name().lower():
                # return cam
                self.__console__.info("{} Camera '{}' object getted".format(self.__classname__, name))
                return camera_in_list
        # else return None
        self.__console__.error("{} Camera '{}' object not found".format(self.__classname__, name))
        return None



    def add_camera(self, name: str, index: str) -> None:
        try:
            # init a new camera object
            cam = CameraObject(self.__kernel__, self._cameras_feed_folder, self._cameras_setting_folder, name, index)
            # start the cam if possible else raise error and catch it
            cam.start()
            # add the cam to cams list
            self.CAMERAS_LIST.append(cam)
            # add 1 to cams count
            self._camera_count += 1
            self.__console__.info("{} Camera '{}' added".format(self.__classname__, name))
        except Exception as e:
            self.__console__.error("{} Error while adding camera {} : {}".format(self.__classname__, name, e))

    def remove_camera(self, cam_name: str) -> None:
        self.__console__.info("{} Removing camera '{}'".format(self.__classname__, cam_name))
        # get cam object
        cam = self.get_camera_by_name(cam_name)
        if cam is not None:  # if object is not none
            # remove camera
            cam.remove()
            self.__remove_camera_from_list(cam_name)
            self.__console__.info("{} camera '{}' removed".format(self.__classname__, cam_name))

    def stop_all_cameras(self) -> None:
        self.__console__.info("{} Stopping every camera".format(self.__classname__))

        for camera_in_list in self.CAMERAS_LIST:  # getting every cams
            try:
                # stop cam with the CameraObject function
                camera_in_list.stop()
                self.__console__.info("{} Stopping camera '{}'".format(self.__classname__, camera_in_list))

            except Exception as e:
                self.__console__.info("{} Error while Stopping camera {} : {}".format(self.__classname__, camera_in_list, e))
                continue



    def __remove_camera_from_list(self, cam_name: str):
        # removing camera from list
        for cam_in_list in self.CAMERAS_LIST:  # search camera in list
            # if cam name is in list
            if cam_name == cam_in_list.get_name():
                # removing from list
                self.CAMERAS_LIST.remove(cam_in_list)
                break

    def __load_all_cameras(self):
        # loading camera at startup
        # list every cam setting file
        for setting_file in os.listdir(self._cameras_setting_folder):
            # verify if its a json
            if setting_file.endswith(".json"):
                # getting pth file
                setting_file_path = os.path.join(self._cameras_setting_folder, setting_file)
                # open the json file
                with open(setting_file_path, "r+") as cam_json:
                    # loading json
                    try:
                        setting = json.load(cam_json)
                        # close the file
                        cam_json.close()

                        # store settings
                        name = setting['name']
                        index = setting['index']
                        # adding camera
                        self.add_camera(name, index)
                    except:
                        FileController.remove_file(setting_file_path)
                        continue
