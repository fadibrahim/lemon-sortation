# import the necessary packages
# from collections import deque
import numpy as np
import serial
import time
import argparse
# import imutils
import cv2


arduino = serial.Serial('COM3', baudrate = 115200, timeout=1) #ganti COM sama COM Arduino di PC
 
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'belum matang':(35, 95, 35),'matang':(0, 91, 195), 'setengah matang':(28,0,76) } #assign new item lower['blue'] = (93, 10, 0)
upper = {'belum matang':(74,255,255),'matang':(26,255,255), 'setengah matang':(32,241,223) } 
 
# define standard colors for circle around the object
colors = {'belum matang':(0,255,0), 'matang':(0, 255, 217), 'setengah matang':(255,0,0)}

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)   
 
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #for each color in dictionary check object in 'frame'
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
        # find contours in the mask and initialize the current
        # (x, y) center of the lemon
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
            # only proceed if the radius meets a minimum size. Correct this value for your object's size
            if radius > 50:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,"lemon " + key, (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
        
                #print (key)

                if key == "matang" : 
                    Lemon = 1
                    arduino.write(str(Lemon).encode('utf-8'))
                    print (Lemon)
                    time.sleep(0.1)

                else:
                    Lemon = 0 
                    arduino.write(str(Lemon).encode('utf-8'))
                    print (Lemon)
                    time.sleep(0.1)
                
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("hsv", hsv)
    cv2.imshow("mask", mask)
    cv2.imshow("blurred", blurred )

  
    #print (Lemon)
    controlkey = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if controlkey == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
