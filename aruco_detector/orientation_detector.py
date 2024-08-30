import cv2
import numpy as np


ORIENTATION_DICT = {'bottom_right': 0, 'bottom_left': 90, 'top_left': 180, 'top_right': 270}


class Picture:
    def __init__(self, image):
        self.image = self.create_image(image)

    @staticmethod
    def create_image(image):
        if isinstance(image, str):
            return cv2.imread(image)
        elif isinstance(image, np.ndarray):
            return image


class OrientationDetector:
    def __init__(self):
        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self.aruco_parameters = cv2.aruco.DetectorParameters()

    def detect_orientation_with_aruco(self, picture: Picture, scale_factor=0.5) -> int:
        self.aruco_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self.aruco_parameters = cv2.aruco.DetectorParameters()
        image_resized = cv2.resize(picture.image, (int(picture.image.shape[1] * scale_factor),
                                                   int(picture.image.shape[0] * scale_factor)))
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image=image_resized, parameters=self.aruco_parameters,
                                                           dictionary=self.aruco_dictionary)

        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (top_left, top_right, bottom_right, bottom_left) = corners
                top_right = (int(top_right[0]), int(top_right[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                top_left = (int(top_left[0]), int(top_left[1]))
                dict_corners = {'top_left': top_left, 'top_right': top_right, 'bottom_left': bottom_left,
                                'bottom_right': bottom_right}
                max_corner = 0
                max_corner_name = ''
                for corner in dict_corners:
                    corner_array = np.array(dict_corners[corner])
                    norm = np.linalg.norm(corner_array)
                    if norm > max_corner:
                        max_corner = norm
                        max_corner_name = corner
                return ORIENTATION_DICT[max_corner_name]
        else:
            raise Exception('No aruco markers detected')

    @staticmethod
    def crop_image(picture: Picture, y1: int, y2: int, x1: int, x2: int) -> Picture:
        cropped_image = Picture(picture.image[y1: y2, x1:x2])
        return cropped_image
