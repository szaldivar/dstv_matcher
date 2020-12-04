import cv2
from pprint import pprint
from parser.dstv_object import Dstv_object
from DSTVimage import getObjectImg

test = Dstv_object("./parser/pt60.nc1")

im = getObjectImg(test)

cv2.imshow("Test", im)
cv2.waitKey(0)
cv2.destroyWindow("Test")
