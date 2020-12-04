import cv2
import math
import numpy as np

TARGET_SIZE = 1000

def drawContours(obj, offset, im_X, im_Y, im, scaling):
    for contour in obj.external_contours:
        arr = []
        for point in contour:
            q_point = point["q"]*scaling
            x_point = point["x"]*scaling
            if (point["reference"] == "bottom"):
                y = im_Y - (offset + q_point)
            elif (point["reference"] == "top"):
                y = offset + q_point
            else:
                y = im_Y - (offset + q_point)
            x = offset + x_point
            arr.append([x, y])
        a3 = np.array([arr], dtype=np.int32 )
        cv2.fillPoly( im, a3, 255 )

def drawHoles(obj, offset, im_X, im_Y, im, scaling):
    if (not obj.holes):
        return
    for hole in obj.holes:
        q_point = hole["q"]*scaling
        x_point = hole["x"]*scaling
        d_point = hole["d"]*scaling
        slotted_y = round(hole["s_height"]*scaling)
        slotted_x = round(hole["s_width"]*scaling)
        if (hole["reference"] == "bottom" or 
            hole["reference"] == "axis"):
            y = im_Y - (offset + q_point)
            slotted_y = -slotted_y
        else:
            y = offset + q_point
        x = offset + x_point
        x = round(x)
        y = round(y)
        r = round(d_point/2)
        # draw 4 circles, one for each corner
        for aux_x in [x, x+slotted_x]:
            for aux_y in [y, y+slotted_y]:
                cv2.circle(im, (aux_x,aux_y), r, 0, -1)
        # draw 2 rectangles to connect the circles
        to_rec_1 = [
            (x-r, y),
            (x+slotted_x+r, y+slotted_y)
        ]
        to_rec_2 = [
            (x, y+r),
            (x+slotted_x, y+slotted_y-r)
        ]
        cv2.rectangle(im, to_rec_1[0], to_rec_1[1], 0, -1)
        cv2.rectangle(im, to_rec_2[0], to_rec_2[1], 0, -1)

def getObjectImg(obj):
    # get dimensions
    if (obj.profile_description == None):
        return None
    length = obj.profile_description["length"]
    if "," in length:
        length = length.split(",")[0]
    try:
        length = float(length)
    except:
        return None
    try:
        height = float(obj.profile_description["profile_height"])
    except:
        return None
    offset_x = math.ceil(length*0.1)
    offset_y = math.ceil(height*0.1)
    offset = max(offset_x, offset_y)
    im_X = math.ceil(length+2*offset)
    im_Y = math.ceil(height+2*offset)
    scaling = TARGET_SIZE/max(im_X, im_Y)
    im_X = round(im_X * scaling)
    im_Y = round(im_Y * scaling)
    offset = round(offset * scaling)
    im = np.zeros([im_Y, im_X], dtype=np.uint8)
    drawContours(obj, offset, im_X, im_Y, im, scaling)
    drawHoles(obj, offset, im_X, im_Y, im, scaling)
    return im
