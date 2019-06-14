import cv2
import numpy as np
import sys

def checkAndChangeValue():
    global refPt
    if(refPt != [] and len(refPt)==2):
        global x 
        global y
        x, y = refPt[0] 
        global width
        global height
        xEnd, yEnd = refPt[1]
        if xEnd < x:
            width = x - xEnd
            x = xEnd
        else:
            width = xEnd - x
        if yEnd < y:
            height = y - yEnd
            y = yEnd
        else:
            height = yEnd - y

        refPt = []
        initialize()


def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting (x, y) coordinates
	if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            return
            
        
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
            refPt.append((x, y))
            checkAndChangeValue()
            return
            

def initialize():
    global roi_hist,term_criteria,frame,hasInit
    if hasInit == False:
        roi = frame[y: y + height, x: x + width]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
        roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        hasInit = True

camera = True

frame = None
hasInit = False
x = y = width = height = 0
term_criteria = None
roi_hist = None

def main():
    global camera
    if len(sys.argv) == 2:
        camera = False
    else:
        camera = True
    if camera == False:
        video = cv2.VideoCapture(sys.argv[1])


    if camera ==  True:
        cap = cv2.VideoCapture(0)

    refPt = []

    while True:
        global frame,hasInit,x,y
        if camera == True:
            _, frame = cap.read()
        else:
            _, frame = video.read()
        

        if hasInit == True :
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            _, track_window = cv2.meanShift(mask, (x, y, width, height), term_criteria)
            x, y, w, h = track_window
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        #cv2.imshow("Mask", mask)
        cv2.setMouseCallback("Frame", click_and_crop)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(60)
        if key == 27:
            break
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()