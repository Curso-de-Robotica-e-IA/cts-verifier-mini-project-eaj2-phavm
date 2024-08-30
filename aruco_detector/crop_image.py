import cv2


crop_camera_preview = [(102, 240), (919, 240), (919, 852), (102, 852)]
crop_oriented_photo = [(920, 240), (1735, 240), (919,853), (1735, 853)]

CAMERA_PREVIEW_CORDS = (240, 852, 102, 919)
ORIENTED_PHOTOS_CORDS = (240, 853, 920, 1735)


def crop_image(y1, y2, x1, x2):
    img = cv2.imread('cameraorientationscreen.png')
    crop_img = img[y1: y2, x1:x2]
    cv2.imshow('img', crop_img)
    cv2.waitKey(0)


crop_image(*ORIENTED_PHOTOS_CORDS)
