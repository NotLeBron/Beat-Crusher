import cv2, copy, math

import numpy as np


class DrumStick(object):

    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
        

        cv2.namedWindow('controls', cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow('controls',500, 500)
        """cv2.createTrackbar('rm','controls',167,255,self.nothing)
        cv2.createTrackbar('gm','controls',118,255,self.nothing)
        cv2.createTrackbar('bm','controls',0,255,self.nothing)

        cv2.createTrackbar('rf','controls',255,255,self.nothing)
        cv2.createTrackbar('gf','controls',255,255,self.nothing)
        cv2.createTrackbar('bf','controls',255,255,self.nothing)"""

        #OPTIMAL VALUES TO DETECT RED COLOR
        self.RED_MIN = np.array([167, 118, 0])
        self.RED_MAX = np.array([255, 255 ,255])

        self.BLUE_MIN = np.array([74, 163, 0])
        self.BLUE_MAX = np.array([114, 255 ,255])


        self.frame = None
        self.redStickContour = None
        self.blueStickContour = None


    def run(self):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame, 1)

        frame = self.sameRatioResize(frame, 2560, 1440)

        
        self.filterFrame('red', copy.deepcopy(frame), self.RED_MIN, self.RED_MAX)
        self.filterFrame('blue', copy.deepcopy(frame), self.BLUE_MIN, self.BLUE_MAX)

        contours = [self.blueStickContour, self.redStickContour]

        try:

            self.frame = cv2.drawContours(frame,contours[0],0,(0,255,0),2)
            self.frame = cv2.drawContours(frame,contours[1],0,(0,255,0),2)
        except:
            pass

        return self.frame

    def getFrame(self):
        return self.frame

    def filterFrame(self, color, rawFrame, colorMin, colorMax):
        if rawFrame is None:return
        hsvFrame = cv2.cvtColor(rawFrame, cv2.COLOR_BGR2HSV)

        newFrame = cv2.inRange(hsvFrame, colorMin, colorMax)

        contours, hierarchy = cv2.findContours(image=newFrame, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        newFrame = newFrame.copy()
        newFrame = cv2.cvtColor(newFrame, cv2.COLOR_GRAY2BGR) 

        try:
            largestContour = max(contours, key = cv2.contourArea)

            """largeContours = []

            avgP1X = 0
            avgP1Y = 0
            avgP2X = 0
            avgP2Y = 0
            avgP3X = 0
            avgP3Y = 0
            avgP4X = 0
            avgP4Y = 0
            

            for c in contours:
                rect = cv2.minAreaRect(largestContour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                boxArea = getPolyArea(box)
                

                if boxArea > 2500:
                    largeContours.append(c)

                    avgP1X += box[0][0]
                    avgP1Y += box[0][1]
                    avgP2X += box[1][0]
                    avgP2Y += box[1][1]
                    avgP3X += box[2][0]
                    avgP3Y += box[2][1]
                    avgP4X += box[3][0]
                    avgP4Y += box[3][1]

            avgP1X /= len(largeContours)
            avgP1Y /= len(largeContours)
            avgP2X /= len(largeContours)
            avgP2Y /= len(largeContours)
            avgP3X /= len(largeContours)
            avgP3Y /= len(largeContours)
            avgP4X /= len(largeContours)
            avgP4Y /= len(largeContours)"""

            rect = cv2.minAreaRect(largestContour)
            box = cv2.boxPoints(rect) 
            nbox = np.int0(box)
            boxArea = self.getPolyArea(nbox)

            if boxArea > 2500:
                #cv2.drawContours(newFrame,[nbox],0,(0,255,0),2)

                if color == 'red':
                    self.redStickContour = [nbox]

                elif color == 'blue':
                    self.blueStickContour = [nbox]


            elif boxArea > 100:
                #print('weak SIGNAL - RED STICK')
                pass

        except:
            #print('NO SIGNAL - RED STICK')
            pass

        
        return newFrame


    def getPolyArea(self, poly):
        #https://keisan.casio.com/exec/system/1322718857   formula for area of inscribed quad 

        pA = poly[0]
        pB = poly[1]
        pC = poly[2]
        pD = poly[3]

        sideAB = math.sqrt((pB[0]-pA[0])**2 + (pB[1]-pA[1])**2)
        sideBC = math.sqrt((pC[0]-pB[0])**2 + (pC[1]-pB[1])**2)
        sideCD = math.sqrt((pD[0]-pC[0])**2 + (pD[1]-pC[1])**2)
        sideAD = math.sqrt((pD[0]-pA[0])**2 + (pD[1]-pA[1])**2)

        perimeter = sideAB + sideBC + sideCD + sideAD

        semiPerimeter = perimeter/2

        return math.sqrt( (semiPerimeter-sideAB) * (semiPerimeter-sideBC) * (semiPerimeter-sideCD) * (semiPerimeter-sideAD))

    """def nothing(x):
        pass"""


    def getRedStickTip(self):
        if self.redStickContour is None: return

        avgX = (self.redStickContour[0][1][0] + self.redStickContour[0][2][0])/2
        avgY = (self.redStickContour[0][1][1] + self.redStickContour[0][2][1])/2

        return (avgX, avgY)

    def getBlueStick(self):

        if self.redStickContour is None: return

        avgX = (self.redStickContour[1][1][0] + self.redStickContour[1][2][0])/2
        avgY = (self.redStickContour[1][1][1] + self.redStickContour[1][2][1])/2

        return (avgX, avgY)


    def sameRatioResize(self, frame, width, height):

        if frame is None:return
        fW = frame.shape[0]
        fH = frame.shape[1]

        
        widthRatio = int(fW/width)
        heightRatio = int(fH/height)

        dim = (width, height)

        return cv2.resize(frame, dim, fy=heightRatio, interpolation=cv2.INTER_AREA)
            

        pass






