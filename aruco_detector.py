import cv2
import numpy as np

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
parameters = cv2.aruco.DetectorParameters()
image = cv2.imread('aruco_rot90.jpg')
scale_factor = 0.7
image = cv2.resize(image, (int(image.shape[1] * scale_factor), int(image.shape[0] * scale_factor)))
(corners, ids, rejected) = cv2.aruco.detectMarkers(image=image, parameters=parameters, dictionary=dictionary)

# verify *at least* one ArUco marker was detected
if len(corners) > 0:
    # flatten the ArUco IDs list
    ids = ids.flatten()
    # loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))  # ((x,y), (x,y), (x,y), (x,y))
        (top_left, top_right, bottom_right, bottom_left) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        top_right = (int(top_right[0]), int(top_right[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
        top_left = (int(top_left[0]), int(top_left[1]))

        dict_corners = {'top_left': top_left, 'top_right': top_right, 'bottom_left': bottom_left,
                        'bottom_right': bottom_right}
        max_corner = 0
        for corner in dict_corners:
            corner_array = np.array(dict_corners[corner])
            norm = np.linalg.norm(corner_array)
            if norm > max_corner:
                max_corner = norm
                max_corner_name = corner
        print(max_corner_name)
        # draw the bounding box of the ArUCo detection
        cv2.line(image, top_left, top_right, (0, 255, 0), 2)
        cv2.line(image, top_right, bottom_right, (0, 255, 0), 2)
        cv2.line(image, bottom_right, bottom_left, (0, 255, 0), 2)
        cv2.line(image, bottom_left, top_left, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the ArUco
        # marker
        c_x = int((top_left[0] + bottom_right[0]) / 2.0)
        c_y = int((top_left[1] + bottom_right[1]) / 2.0)
        cv2.circle(image, (c_x, c_y), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the image
        cv2.putText(image, str(markerID),
                    (top_left[0], top_left[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        print("[INFO] ArUco marker ID: {}".format(markerID))


# detecting the order in images:





    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
