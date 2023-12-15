import cv2
import numpy as np
from cv2 import aruco

# Size and offset value
size = 150
offset = 0
x_offset = y_offset = int(offset) // 2

# get dictionary and generate image
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
ar_img = aruco.generateImageMarker(dictionary, 49, size)

# make white image
img = np.zeros((size + offset, size + offset), dtype=np.uint8)
img += 255

# overlap image
img[y_offset:y_offset + ar_img.shape[0], x_offset:x_offset + ar_img.shape[1]] = ar_img

cv2.imwrite("marker_3.png", img)