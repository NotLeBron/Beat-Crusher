import cv2, copy, math

import numpy as np

from PIL import Image, ImageTk

class DrumStick(object):

    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
        

        """cv2.namedWindow('controls', cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow('controls',500, 500)"""
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
            #light
            #self.frame = self.processFrame(frame)


            #object
            self.frame = cv2.drawContours(frame,contours[0],0,(0,255,0),2)
            self.frame = cv2.drawContours(frame,contours[1],0,(0,255,0),2)
        except:
            pass

        return self.frame

    
    def opencvToTk(self, frame):
        #from cmu_112_graphics_openCV
        if frame is None: return

        frame = self.sameRatioResize(frame, 500, 281)
        """Convert an opencv image to a tkinter image, to display in canvas."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_image)
        tkImage = ImageTk.PhotoImage(image=pil_img)
        return tkImage

    def getCopyTKFrame(self):
        tkImage = self.opencvToTk(copy.deepcopy(self.frame))
        return tkImage

    def filterFrame(self, color, rawFrame, colorMin, colorMax):
        #https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html
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

            if boxArea > 3000:
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

    def processFrame(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #remove everything but bright white light
        bwFrame = cv2.threshold(frame, 250, 255, cv2.THRESH_BINARY)[1]
        
        #erode away at the edges of light
        erodedFrame = cv2.erode(bwFrame,None,iterations=5)

        #decreases size of lights
        dilatedFrame = cv2.dilate(erodedFrame,None,iterations=5)

        


        #draws circle around light spots
        contours, hierarchy = cv2.findContours(image=dilatedFrame, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        finalImg = dilatedFrame.copy()
        finalImg = cv2.cvtColor(finalImg, cv2.COLOR_GRAY2BGR) 

        try:
            largestContour = max(contours, key = cv2.contourArea)
            rect = cv2.minAreaRect(largestContour)
            box = cv2.boxPoints(rect) 
            nbox = np.int0(box)
            boxArea = self.getPolyArea(nbox)

            if boxArea > 3000:
                cv2.drawContours(finalImg,[nbox],0,(0,255,0),2)

                return finalImg


            elif boxArea > 100:
                #print('weak SIGNAL - RED STICK')
                pass

        except:
            pass




        cv2.drawContours(image=finalImg, contours=self.contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

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

        
        #[array][point][x or y] .......0 required for array
        avgX = (self.redStickContour[0][0][0] + self.redStickContour[0][1][0])/2
        avgY = (self.redStickContour[0][0][1] + self.redStickContour[0][1][1])/2

        avgX2 = (self.redStickContour[0][2][0] + self.redStickContour[0][3][0])/2
        avgY2 = (self.redStickContour[0][2][1] + self.redStickContour[0][3][1])/2

        absX = (avgX + avgX2) /2
        absY = min(float(avgY) , float(avgY2))


        """print(self.redStickContour, 'step1')
        print(self.redStickContour[0], 'step2')
        print(self.redStickContour[0][0], 'step3')
        print(self.redStickContour[0][0][0], 'step4')"""

        return (absX, absY)

    def getBlueStickTip(self):

        if self.blueStickContour is None: return

        
        #[array][point][x or y] .......0 required for array
        avgX = (self.blueStickContour[0][0][0] + self.blueStickContour[0][1][0])/2
        avgY = (self.blueStickContour[0][0][1] + self.blueStickContour[0][1][1])/2

        avgX2 = (self.blueStickContour[0][2][0] + self.blueStickContour[0][3][0])/2
        avgY2 = (self.blueStickContour[0][2][1] + self.blueStickContour[0][3][1])/2

        absX = (avgX + avgX2) /2
        absY = min(float(avgY) , float(avgY2))


        """print(self.redStickContour, 'step1')
        print(self.redStickContour[0], 'step2')
        print(self.redStickContour[0][0], 'step3')
        print(self.redStickContour[0][0][0], 'step4')"""

        return (absX, absY)


    def sameRatioResize(self, frame, width, height):

        if frame is None:return
        fW = frame.shape[0]
        fH = frame.shape[1]

        
        widthRatio = int(fW/width)
        heightRatio = int(fH/height)

        dim = (width, height)

        return cv2.resize(frame, dim, fy=heightRatio, interpolation=cv2.INTER_AREA)
            

        pass