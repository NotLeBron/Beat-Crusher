from cmu_112_graphics import *

import pygame

class DrumPiece(object):

    def __init__(self, timeStamp, ticksPerSec, types, timeCreated, fps, scale=.01):
        #print(currTime)
        #self.timeOnCreation = currTime
        self.types = types
        self.offset = 2 
        self.timeStamp = timeStamp
        self.timeStampSeconds = (self.timeStamp * ticksPerSec)/1000 + self.offset
        self.havePlayed  = False
        
        self.timeCreated = timeCreated
        self.scale = scale


        #changes with framerate (game performance)
        #if performance dips (framerate goes down) objects should grow faster to compensate and vice versa
        #not perfect - slow to fix animation synchronization
        #TODO: 
        if fps > 5:
            self.growthRate = self.calcGrowthRate() /(19 - 19/fps)

        else:
            #first few seconds framerate will be inacurrate until it averages out
            self.growthRate = self.calcGrowthRate() /(19 - 19/5)


        if types == 'hihat':
            self.sound = pygame.mixer.Sound("Resources/Audio files/hihat.mp3")

        elif types == 'snare':
            self.sound = pygame.mixer.Sound("Resources/Audio files/snare.mp3")

        elif types == 'high':
            self.sound = pygame.mixer.Sound("Resources/Audio files/highTom.mp3")

        elif types == 'mid':
            self.sound = pygame.mixer.Sound("Resources/Audio files/midTom.mp3")

        elif types == 'floor':
            self.sound = pygame.mixer.Sound("Resources/Audio files/floorTom.mp3")

        elif types == 'cymb':
            self.sound = pygame.mixer.Sound("Resources/Audio files/cymb.mp3")


    def calcGrowthRate(self):


        self.lifespan = (self.timeStampSeconds-self.timeCreated)
        maxScale = 1.19
        
        return (maxScale-self.scale)/self.lifespan


    def grow(self):
        self.scale += self.growthRate

    def playSound(self):

        if self.havePlayed == False:
            if self.types == 'snare':
                pygame.mixer.Channel(0).play(self.sound, maxtime=500)
                return 'played'

            elif self.types == 'hihat':
                pygame.mixer.Channel(1).play(self.sound, maxtime=500)
                return 'played'

            elif self.types == 'cymb':
                pygame.mixer.Channel(2).play(self.sound)
                return 'played'

            elif self.types == 'floor':
                pygame.mixer.Channel(3).play(self.sound)
                return 'played'
            
            elif self.types == 'high':
                pygame.mixer.Channel(4).play(self.sound)
                return 'played'

            elif self.types == 'mid':
                pygame.mixer.Channel(5).play(self.sound)
                return 'played'

        return 'not played'

    def changeStatus(self):
        self.havePlayed =True

    def checkHit(self, redx, redy, bluex, bluey):
        
        return False
        

    def getTimeStamp(self):
        return self.timeStamp


    def scaleObject(self, scale):
        self.scale = scale

    def getName(self):
        return self.types

    def drawObject(self, app, canvas):

        pass

class Snare(DrumPiece):

    def __init__(self, timeStamp, ticksPerSec, types, timeCreated, fps):
        super().__init__(timeStamp, ticksPerSec, types, timeCreated, fps)

    
    def checkHit(self, redx, redy, bluex, bluey):
        
        #369.1, 785.41, 630.9, 880.59
        if ((redx <= 630.9 and redx >= 369.1 and
            redy <= 880.59 and redy >= 785.41) or 
            (bluex <= 630.9 and bluex >= 369.1 and
            bluey <= 880.59 and bluey >= 785.41)):

            return True


        return False


    
    def drawObject(self, app, canvas):
        if self.scale > 1.19:
            self.scale = 1.19

        x = 500 
        y = 700 *self.scale

        yRad = 40 *self.scale
        xRad = 110 *self.scale

        shadowShift = 80 *self.scale

        bodyColor = '#313638'
        topColor = '#DEE5E5'
        trimColor = "white"

        
        #base*
        canvas.create_oval(x+xRad, (y+shadowShift)+yRad, x-xRad, (y+shadowShift)-yRad, fill=bodyColor, width=8*self.scale, outline=trimColor)

        #body
        canvas.create_rectangle(x-xRad+4*self.scale, y, x+xRad-4*self.scale, y+shadowShift, fill=bodyColor, outline=bodyColor)

        #body decor
        canvas.create_line(x+(0), y, x, y+120*self.scale, width = 5*self.scale, fill=trimColor)
        canvas.create_line(x-60*self.scale, y, x-60*self.scale, y+113*self.scale, width = 5*self.scale, fill=trimColor)
        canvas.create_line(x-100*self.scale, y, x-100*self.scale, y+98*self.scale, width = 3*self.scale, fill=trimColor)

        canvas.create_line(x+60*self.scale, y, x+60*self.scale, y+113*self.scale, width = 5*self.scale, fill=trimColor)
        canvas.create_line(x+100*self.scale, y, x+100*self.scale, y+98*self.scale, width = 3*self.scale, fill=trimColor)

        #top
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, outline=trimColor,width=11*self.scale)
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, fill=topColor)
        pass

class Tom(DrumPiece):

    def __init__(self, timeStamp, ticksPerSec,  types, timeCreated, fps):
        super().__init__(timeStamp, ticksPerSec, types, timeCreated, fps)

        self.type = types

    def checkHit(self, redx, redy, bluex, bluey):
        if self.types == 'mid':
            #569.1, 499.81, 830.9, 690.19
            if ((redx <= 830.9 and redx >= 569.1 and
                redy <= 690.19 and redy >= 499.81) or 
                (bluex <= 830.9 and bluex >= 569.1 and
                bluey <= 690.19 and bluey >= 499.81)):

                return True

        elif self.types == 'high':
            #869.1, 595-95.19, 1130.9, 690.19
            if ((redx <= 1580.9 and redx >= 869.1 and
                redy <= 1130.9 and redy >= 499.81) or 
                (bluex <= 1580.9 and bluex >= 869.1 and
                bluey <= 1130.9 and bluey >= 499.81)):

                return True

        elif self.types == 'floor':
            #1041.5, 702.11, 1398.5, 892.49
            if ((redx <= 1398.5 and redx >= 1041.5 and
                redy <= 892.49 and redy >= 702.11) or 
                (bluex <= 1398.5 and bluex >= 1041.5 and
                bluey <= 892.49 and bluey >= 702.11)):

                return True

        return False


    def drawObject(self, app, canvas):
        if self.scale > 1.19:
            self.scale = 1.19

        y = 500 *self.scale
        shadowShift = 160 *self.scale
        yRad = 80 *self.scale
        xRad = 110 *self.scale

        if(self.type == 'mid'):
            x = 700
            topColor = '#3C4767'
        elif(self.type == 'high'):
            x = 1000
            topColor = '#282F44'
        elif(self.type == 'floor'):
            x = 1260
            shadowShift = 250 *self.scale
            y = 670 *self.scale
            topColor = '#776885'
            xRad = 150 *self.scale


        bodyColor = '#313638'
        trimColor = "white"

        
        #base*
        canvas.create_oval(x+xRad, (y+shadowShift)+yRad, x-xRad, (y+shadowShift)-yRad, fill=bodyColor, width=8*self.scale, outline=trimColor)

        #body
        canvas.create_rectangle(x-xRad+4*self.scale, y, x+xRad-4*self.scale, y+shadowShift, fill=bodyColor, outline=bodyColor)

        #body decor

        canvas.create_line(x+(0), y, x, y+(shadowShift+yRad), width = 5*self.scale, fill=trimColor)
        canvas.create_line(x-60*self.scale, y, x-60*self.scale, y+(shadowShift+yRad-10*self.scale), width = 5*self.scale, fill=trimColor)
        canvas.create_line(x-100*self.scale, y, x-100*self.scale, y+(shadowShift+yRad-50*self.scale), width = 3*self.scale, fill=trimColor)

        canvas.create_line(x+60*self.scale, y, x+60*self.scale, y+(shadowShift+yRad-10*self.scale), width = 5*self.scale, fill=trimColor)
        canvas.create_line(x+100*self.scale, y, x+100*self.scale, y+(shadowShift+yRad-50*self.scale), width = 3*self.scale, fill=trimColor)

        #top
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, outline=trimColor,width=11*self.scale)
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, fill=topColor)
        pass

class CrashCymbol(DrumPiece):

    def __init__(self, timeStamp, ticksPerSec,  types, timeCreated, fps):
        super().__init__(timeStamp, ticksPerSec, types, timeCreated, fps)

    def checkHit(self, redx, redy, bluex, bluey):

        #1450-130.9, 333.2-47.59, 1450+130.9, 333.2+47.59
        if ((redx <= 1580.9 and redx >= 1319.1 and
            redy <= 380.67 and redy >= 285.73) or 
            (bluex <= 1580.9 and bluex >= 1319.1 and
            bluey <= 380.67 and bluey >= 285.73)):

            return True

        return False


    def drawObject(self, app, canvas):
        if self.scale > 1.19:
            self.scale = 1.19
        x = 1450
        y = 280 *self.scale

        yRad = 40 *self.scale
        xRad = 110 *self.scale

        #shifts shadow a few pixels down
        shadowShift = 7 *self.scale

        
        
        canvas.create_oval(x+xRad, (y+shadowShift)+yRad, x-xRad, (y+shadowShift)-yRad, fill='black')
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, fill='pink')
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, width= 10,outline='pink')

        for i in range(12):
            xRad /= 1.2
            yRad /= 1.2
            canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad)

class HiHat(DrumPiece):

    def __init__(self, timeStamp, ticksPerSec, types, timeCreated, fps):
        super().__init__(timeStamp, ticksPerSec, types, timeCreated, fps)

    def checkHit(self, redx, redy, bluex, bluey):

        #390.9, 499.79, 129.1, 404.61
        if ((redx <= 390.9 and redx >= 129.1 and
            redy <= 499.79 and redy >= 404.61) or 
            (bluex <= 390.9 and bluex >= 129.1 and
            bluey <= 499.79 and bluey >= 404.61)):

            return True

        return False

    def drawObject(self, app, canvas):

        #dont get bigger than this
        if self.scale > 1.19:
            self.scale = 1.19

        x = 260
        y = 380 *self.scale

        yRad = 40 *self.scale
        xRad = 110 *self.scale

        #shifts shadow 7 pixels down
        shadowShift = 7 *self.scale
        
        canvas.create_oval(x+xRad, (y+shadowShift)+yRad, x-xRad, (y+shadowShift)-yRad, fill='black')
        canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad, fill='purple')
        
        #ring texture for top
        for i in range(12):
            xRad /= 1.2
            yRad /= 1.2
            canvas.create_oval(x+xRad, y+yRad, x-xRad, y-yRad)



def createObject(timeStamp, kind, timeCreated, song, fps, ticksPerSec = 60000/(116*384)):

    if song == 'Smells Like Teen Spirit':
        ticksPerSec = 60000/(116*384)

    if song == 'Boulevard of Broken Dreams':
        ticksPerSec = 60000/(83*480)

    if kind == 'snare':
        return Snare(timeStamp, ticksPerSec, 'snare', timeCreated, fps)

    elif kind == 'hihat':
        return HiHat(timeStamp, ticksPerSec, 'hihat', timeCreated, fps)

    elif kind == 'mid':
        return Tom(timeStamp, ticksPerSec,'mid', timeCreated, fps)

    elif kind == 'high':
        return Tom(timeStamp, ticksPerSec,'high', timeCreated,fps)

    elif kind == 'cymb':
        return CrashCymbol(timeStamp, ticksPerSec, 'cymb', timeCreated, fps)

    elif kind == 'floor':
        return Tom(timeStamp, ticksPerSec, 'floor', timeCreated, fps)

    

def checkStatus(app, currTime):
    pass

def drawObjects(app, canvas):

    for beat in app.beatsOnScreen:
        beat.drawObject(app, canvas)


def destroyObjects(app):

    if len(app.beatsOnScreen) <= 0: return
    beatsTimeInSeconds = round(app.beatsOnScreen[0].timeStampSeconds, 3)

    if beatsTimeInSeconds < app.songTime+.05 and beatsTimeInSeconds > app.songTime:
        
        try:
            if app.beatsOnScreen[0].checkHit(app.redStick[0], app.redStick[1], app.blueStick[0], app.blueStick[1]):
                app.combo += 1
                app.earlyHits += 1
                if app.combo not in app.comboDict:
                    app.comboDict[app.combo] = 0
                else:
                    app.comboDict[app.combo] += 1
                
                app.drumAudio.addWork(app.beatsOnScreen[0].getName())
                app.beatsOnScreen.pop(0)
                return

            else:
                pass

        except:
            pass
        
    if round(app.beatsOnScreen[0].timeStampSeconds, 3) == app.songTime:
        
        try:
            if app.beatsOnScreen[0].checkHit(app.redStick[0], app.redStick[1], app.blueStick[0], app.blueStick[1]):
                app.combo += 1
                app.perfectHits += 1
                if app.combo not in app.comboDict:
                    app.comboDict[app.combo] = 0
                else:
                    app.comboDict[app.combo] += 1

                app.drumAudio.addWork(app.beatsOnScreen[0].getName())
                app.beatsOnScreen.pop(0)
                return

            else:
                pass

        except:
            pass
        
    if round(app.beatsOnScreen[0].timeStampSeconds, 3) < app.songTime-.02:
        
        try:
            if app.beatsOnScreen[0].checkHit(app.redStick[0], app.redStick[1], app.blueStick[0], app.blueStick[1]):
                app.combo += 1
                if app.combo not in app.comboDict:
                    app.comboDict[app.combo] = 0
                else:
                    app.comboDict[app.combo] += 1
                app.lateHits += 1

            else:
                app.misses += 1
                if app.longestCombo < app.combo:
                    app.longestCombo = app.combo
                app.combo = 0
                pass

        except:
            app.misses += 1
            if app.longestCombo < app.combo:
                app.longestCombo = app.combo
            app.combo = 0
            pass
        app.drumAudio.addWork(app.beatsOnScreen[0].getName())
        app.beatsOnScreen.pop(0)
    

def scale(app):
    for beat in app.beatsOnScreen:
        beat.grow()

def checkKickDrum(app):
    """Bass drum backtrack, slightly off """

    if len(app.beatQ.kickBeatMap) > 0:
        beatInSeconds = (app.beatQ.kickBeatMap[0][0] * app.song.getTicksPerSec())/1000 + app.song.offset
        

        """diff = app.songTime - beatInSeconds

        if diff <= .027 and diff >= -.027:
            print(beatInSeconds, app.songTime)
            app.drumAudio.addWork('kick')
            app.beatQ.kickBeatMap.pop(0)

        elif diff > .027:
            print(beatInSeconds, app.songTime)
            app.beatQ.kickBeatMap.pop(0)
            print('missed')"""


        if round(beatInSeconds, 3)  >= app.songTime-.04 and round(beatInSeconds, 3) <= app.songTime +.02:
            app.drumAudio.addWork('kick')
            app.beatQ.kickBeatMap.pop(0)
            

        elif round(beatInSeconds, 3) < app.songTime-.04:
            app.drumAudio.addWork('kick')
            app.beatQ.kickBeatMap.pop(0)
            print('missed')
        



        