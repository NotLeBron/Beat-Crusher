import cv2, threading, time, copy

import numpy as np
#from cmu_112_graphics import *


#TODO: FIX CAMERA CRASHING GAME ON EXIT
class CameraDetector(object):

    def __init__(self):

        self.webcam = cv2.VideoCapture(0)
        self.cameraOpen = True

        self.sens = 255
        self.thresh = 250

        self.contours = None

        cv2.namedWindow('controls')
        cv2.createTrackbar('circ','controls',5,100,self.nothing)
        cv2.createTrackbar('convex','controls',5,100,self.nothing)
        cv2.createTrackbar('inertia','controls',50,100,self.nothing)

        print('cam Thread: init')

    def runFeed(self):

        while self.cameraOpen:
            #capture frame
            ret, capFrame = self.webcam.read()
            #cv2.resize(capFrame, (900, 900))


            

            try:
                cv2.imshow('Input', self.processFrame(capFrame))
            except:
                print ("Caught an exception")
            
            

            #turns off camera if q pressed
            if cv2.waitKey(1) == ord('q'):

                print('camera thread: closing')
            
                
                self.cameraOpen = False
                print('exiting')
                

                break

        cv2.destroyAllWindows()
        print('here')
        for i in range (1,5):
            cv2.waitKey(1)
        
        self.webcam.release()



        



    def changeSens(self, amount):

        self.sens += amount

    def changeThresh(self, amount):

        self.thresh += amount


    def processFrame(self, frame):


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #remove everything but bright white light
        bwFrame = cv2.threshold(frame, 250, 255, cv2.THRESH_BINARY)[1]
        
        #erode away at the edges of light
        erodedFrame = cv2.erode(bwFrame,None,iterations=5)

        #decreases size of lights
        dilatedFrame = cv2.dilate(erodedFrame,None,iterations=5)

        


        #draws circle around light spots
        self.contours, hierarchy = cv2.findContours(image=dilatedFrame, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        finalImg = dilatedFrame.copy()
        finalImg = cv2.cvtColor(finalImg, cv2.COLOR_GRAY2BGR) 
        cv2.drawContours(image=finalImg, contours=self.contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

        """for c in self.contours:

            M = cv2.moments(finalImg)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            #cv2.circle(finalImg, (cX, cY), 1, (0, 0, 255), 2, cv2.LINE_AA)

            print(cX, cY)"""


        


        return finalImg

    def findCenter(self):
        pass

    def nothing(self):
        pass


