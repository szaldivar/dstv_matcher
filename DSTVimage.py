import cv2
import math
import numpy as np

TARGET_SIZE = 1000

def findCenter(actualPoint,prevPoint,radius):
    h = [(actualPoint[0] + prevPoint[0] )/2,(actualPoint[1] + prevPoint[1])/2]

    c = getDistance(h,actualPoint)
    b = abs(h[0]- actualPoint[0])
    a = abs(h[1]- actualPoint[1])

    C = math.sqrt(pow(radius,2)- pow(c,2))

    if(b == 0):
        return (0,0)
        #ta facil
    elif(a == 0):
        return(0,0)
        #ta facil tambien segun
    else:
        scaleFactor = C/c
        A = a * scaleFactor
        B = b * scaleFactor
        if(actualPoint[1] > prevPoint[1]):
            if(actualPoint[0] > prevPoint[0]):
                B = -B
        else:
            A = -A
            if(actualPoint[0] > prevPoint[0]):
                B = -B
        if(radius < 0):
            A = -A
            B = -B
        return (round(h[0] + A),round(h[1] + B))
        


def getDistance(point1,point2):
    a = pow(abs(point1[1] - point2[1]),2)
    b = pow(abs(point1[0] - point2[0]),2)
    c = math.sqrt(a+b)
    return c


def drawNotches(obj, offset, im_X, im_Y, im, scaling):
    for contour in obj.external_contours:
        arr = []
        foundNotch = False
        radius = 0.0
        for point in contour:
            if(foundNotch):
                if (point["reference"] == "bottom" or point["reference"] == "axis"):
                    actualY = im_Y - offset - (point["q"])* scaling
                    prevY = im_Y - offset - (last["q"])*scaling
                else:
                    actualY = offset + (point["q"])* scaling
                    prevY = offset + (last["q"])*scaling

                actualX = offset + (point["x"])*scaling
                prevX = offset + (last["x"])*scaling
                r = last["r"]* scaling
                actual = (actualX,actualY)
                prev = (prevX, prevY)

                foundNotch =  False
                center = findCenter(actual,prev,r)
                print("Centro",center)
                print("Actual",actual)
                print("Prev",prev)
                print("r", r)

                if(r < 0):
                    r_notch = round(-r)
                    cv2.circle(im, center, r_notch, 0, -1)
                else: 
                    r_notch = round(r)
                    cv2.circle(im, center, r_notch, 255, -1)
                         
            if(point["r"] != 0.0):
                last = point
                foundNotch = True
                
                

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
    drawNotches(obj, offset, im_X, im_Y, im, scaling)
    return im
