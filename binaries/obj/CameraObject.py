import os
import time
import json
import numpy as np
import cv2
from threading import Thread
from PIL import Image

from binaries.obj.AiObject import AiObject

from controllers.FileController import FileController
from controllers.FolderController import FolderController
from controllers.TimeController import TimeController
from controllers.DateController import DateController
# ========================================== FIN DES IMPORTS ========================================================= #


class CameraObject(Thread, AiObject):

    def __init__(self, kernel, store_feed_path: str, setting_path: str, name: str, index: str):
        Thread.__init__(self)
        AiObject.__init__(self, kernel)
        self.setDaemon(True)

        # init vars
        self._camera = None
        self._name = name
        self._index = index
        self._live_frame = None

        # init feed folders
        self._camera_feed_folder = os.path.join(store_feed_path, self._name.replace(" ", "_"))
        # init json setting file
        self._camera_setting_file = os.path.join(setting_path, self._name.replace(" ", "_") + ".json")
        # creating folder if they doesnt exist
        FolderController.create_folder(self._camera_feed_folder)
        # creating setting file
        self.__create_setting_file()
        # accessing to camera feed
        self.__init_frame_capture()



    def run(self):
        try:
            # running camera feed
            self.__console__.info("{} Starting '{}' feed".format(self.__classname__, self._name))
            self.__video_feed()

        except Exception as e:
            self.__console__.error("{} Error while starting '{}' feed : {}".format(self.__classname__, self._name, e))
            pass



    def get_name(self) -> str:
        # getting camera name
        return self._name

    def get_live_frame(self) -> str:
        # getting live frame
        return self._live_frame



    def stop(self) -> None:
        try:
            # stopping the opencv cam
            self._camera.release()
            # reset the cam to None
            self._camera = None
            self.__console__.info("{} '{}' Stopped".format(self.__classname__, self._name))
        except:
            self.__console__.info("{} Error while releasing the camera '{}'".format(self.__classname__, self._name))
            pass

    def remove(self) -> None:
        # stop the camera
        self.stop()
        # remove every feed
        self.__remove_all_feed()
        # remove the camera dir
        self.__remove_feeds_folder()
        # remove setting file
        self.__remove_setting_file()
        self.__console__.info("{} '{}' Removed".format(self.__classname__, self._name))



    def __video_feed(self) -> None:
        # running the camera feed
        while True:
            try:
                # if opencv access to camera
                if self._camera is not None:

                    # getting if frame statut, frame
                    is_frame_grabbed, frame = self._camera.read()

                    # if frame statut is not None
                    if is_frame_grabbed:

                        # if frame is not none
                        if frame is not None:
                            """
                            Processing image here
                            """
                            # write date and hour on frame
                            frame = self.__write_datetime_on_frame(frame)
                            # save the frame in web img path
                            self.__save_live_frame(frame)

                            # show the frame for test
                            # self._show_frame(frame)

                        else:
                            continue
                        time.sleep(0.5)

                    else:
                        time.sleep(1.5)
                        continue
                else:
                    break

            except Exception as e:
                self.__console__.error("{} Video feed error, shutting down camera '{}'".format(self.__classname__, self._name))
                self.stop()

    def __save_live_frame(self, frame, file_name: str= "livefeed", extension: str= ".jpg") -> None:
        try:
            # feed img file name
            livefeed_filename = file_name + extension
            # save the frame in img file
            cv2.imwrite(os.path.join(self._camera_feed_folder, livefeed_filename), frame)
            # compresse the saved img
            compressed_img = Image.open(os.path.join(self._camera_feed_folder, livefeed_filename))
            # save the compressed img
            compressed_img.save(os.path.join(self._camera_feed_folder, livefeed_filename), "JPEG", quality=70)
            # setting live frame to file name
            self._live_frame = livefeed_filename
        except Exception as e:
            pass

    def __create_setting_file(self) -> None:
        # create file
        with open(self._camera_setting_file, "w+") as f:
            # write in file
            json.dump(self.__setting_data(), f)
            # close the file
            f.close()

    def __setting_data(self) -> dict:
        return {"name": self._name, "index": self._index}

    def __remove_setting_file(self) -> None:
        # remove setting file
        FileController.remove_file(self._camera_setting_file)

    def __remove_feeds_folder(self) -> None:
        # remove feed folder
        FolderController.remove_folder(self._camera_feed_folder)

    def __remove_all_feed(self) -> None:
        # list feed in cam path
        FileController.remove_all_file_in_folder(self._camera_feed_folder)

    def __init_frame_capture(self) -> None:
        # if index is a number
        if str(self._index).isdigit():
            # transform it to int for cam index else it maybe ip
            self._index = int(self._index)
        try:
            # start opencv cam
            self._camera = cv2.VideoCapture(self._index)
        except:
            pass

    def __write_datetime_on_frame(self, frame):
        font = cv2.FONT_ITALIC  # font style
        font_color = (255, 255, 255)  # font color : white
        font_pos = (10, 30)  # font position
        date = DateController.get_date() + " " + TimeController.get_time()  # create date
        return cv2.putText(frame, date, font_pos, font, 1, font_color, 1, cv2.LINE_AA)

    def __show_frame(self, frame):
        cv2.imshow('frame', frame)
