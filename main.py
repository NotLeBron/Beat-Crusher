from cmu_112_graphics import *
from DrumStickHandler import *
import time, threading, pygame, queue

from MusicHandler import *

import DrumKit


def appStarted(app):
    app.mode = 'menu' #menu

    app.buttonX = app.width//2
    app.playY = app.height//2
    app.scoresY = app.playY + 150
    app.settingsY = app.scoresY + 150
    app.shadowShift = 5
    app.widthRad = 200
    app.heightRad = 40

    app.playShadow = True
    app.timerDelay = 500
    app.menuState = 1

    app.backx = app.width//2 - 800
    app.backy = app.height//2 +400

    app.backXRad = 100

    #app.timerDelay = 500

def gameStarted(app):
    app.mode = 'game'
    app.defualtSong = 'Smells Like Teen Spirit'
    #app.defualtSong = 'Boulevard of Broken Dreams'
    app.gameState = 1
    if app.gameState == 1:
        app.drumstick = DrumStick()
        app.frame = None

        app.totalBeats = songInfo.getTotalBeats(app.defualtSong)

        app.redStick = ()
        app.blueStick = ()
        app.redStickCoord = ()
        app.blueStickCoord = ()

        app.timerDelay = 500

        app.startTime = time.time()
        app.ellipses = 1
        app.isLoading = True

        
        app.isCountDown = False

        app.song = Song(app.defualtSong)
        app.beatQ = BeatQueue(app.defualtSong, 2)
        app.beatsOnScreen = []
        app.currBeat = 0
        app.songOffset = 0



        app.lock = threading.Lock()
        app.camThread = camThread(app)
        #app.gameThread = gameThread(app)
        app.camThread.start()
        #app.gameThread.start()

        

        pygame.mixer.set_num_channels(50)
        app.sound1 = pygame.mixer.Sound("Resources/Audio files/hihat.mp3")
        app.sound2 = pygame.mixer.Sound("Resources/Audio files/snare.mp3")

        app.q = queue.LifoQueue()
        app.maxThreads = 10
        app.songProgress = 0
        app.songTime = 0
        


        app.accuracy = 0
        app.score = 0
        app.hits = 0
        app.misses = 0
        app.earlyHits = 0
        app.lateHits = 0
        app.perfectHits = 0
        app.combo = 0
        app.comboDict = dict()
        app.longestCombo = 0
        app.progress = 0

        app.doOnce_gameCam = False
        app.jobList = [loadingSequence]

        app.frameCount = 0
        app.fps = 0
        app.fpsList = []
        app.timeAtLastCheck = 0
        app.avgFPS = 0
        app.startFPSTracker = False

        app.threads = []



    else:

        pass
    

def updateSongTime(app):
    app.songTime = app.song.getSongTime()

def updateScore(app):
    """
    perfectHit = 1000 points - since very hard
    earlyHit = 100 points
    lateHit = 100 points
    comboBonus = 50 points each
    """
    app.hits = app.perfectHits + app.earlyHits + app.lateHits

    app.score = (app.perfectHits*1000) + (app.earlyHits*100) + (app.lateHits*100) + (sum(app.comboDict.values()) * 50)

def checkGameOver(app):
    if app.songProgress <= 1 and app.songProgress >= .98:
        cv2.destroyAllWindows()
        app.drumstick.capture.release()
        app.song.stop()
        app.camThread.stop()
        calcGrade(app)
        app.gameState = 2
    pass

def calcGrade(app):

    #1000
    pointsPossible = app.totalBeats * 1000 + (app.totalBeats*50)
    grade = ['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']

    percent = .98
    i = 0
    while True:

        if i == 15:
            app.grade = grade[i]
            break
        elif app.score >= pointsPossible*percent:
            print(pointsPossible*percent)
            app.grade = grade[i]
            break
        else:
            if i*100 % 10 == 0:
                percent -= .02
            else:
                percent -= .04
        i += 1




def loadingSequence(app):
    if not app.isCountDown and not app.isLoading: return False
    if app.ellipses > 3:
        app.ellipses = 1
    else:
        app.ellipses += 1
    pass

    if app.isLoading and time.time()-app.startTime > 5:
        app.isLoading = False
        app.isCountDown = True
        app.countDownStartTime = time.time()
        app.countDownNum = 1

    if app.isCountDown:
        if time.time()-app.countDownStartTime > 3:
            
            app.isCountDown = False
            app.timerDelay = 1
            app.songStartTime = time.time() - app.songOffset
            app.song.play()

            app.jobList = [checkGameOver, updateSongTime, updateScore, updateAccuracy, addBeats, 
                        updateSongProgress, app.song.updateSongPosition, DrumKit.destroyObjects, 
                        DrumKit.soundOff, DrumKit.scale ]

            app.startFPSTracker = True
        
            
        else:
            app.countDownNum = 3- int(time.time()-app.countDownStartTime)


    return True

def doWork(item, app):
    item(app)

def worker(app):
    #Help from python queue & multithreadingexample https://gist.github.com/arthuralvim/356795612606326f08d99c6cd375f796
    while True:
        item = app.q.get()
        if item is None:
            break
        item(app)
        app.q.task_done()

def updateFPS(app):

    if int(time.time()) - int(app.timeAtLastCheck) >= 1:
        app.fps = app.frameCount
        app.fpsList.append(app.fps)
        app.avgFPS = sum(app.fpsList)/len(app.fpsList)

        #reset
        app.timeAtLastCheck = time.time()
        app.frameCount = 0

def game_timerFired(app):

    

   
    if app.gameState == 1:
        if app.startFPSTracker == True:

            app.frameCount += 1
            updateFPS(app)


        for i in range(app.maxThreads):
            t = threading.Thread(target=worker, args=(app,))
            t.start()
            app.threads.append(t)


        for item in app.jobList:
            app.q.put(item)

        # block until all tasks are done
        app.q.join()

            
        """if loadingSequence(app): return
        

        updateAccuracy(app)

        
        #print('My: ', getSongTime(app), 'Pygame: ', app.song.getSongTime())
        #app.song.updateSongPosition(getSongTime(app))
        addBeats(app)
        #DrumKit.checkStatus(app, getSongTime(app))
        DrumKit.destroyObjects(app, app.song.getSongTime())
        DrumKit.soundOff(app, getSongTime(app), app.currBeat)
        DrumKit.scale(app)"""
    else:

        pass

def updateAccuracy(app):
    try:
        app.accuracy = round(app.hits/(app.misses + app.hits), 3)
        
    except:
        pass

def game_mousePressed(app, event):
    if app.gameState == 1:
        pygame.mixer.Channel(1).play(app.sound1)
        pygame.mixer.Channel(5).play(app.sound2)
        pass
        #app.song.cymb.play(maxtime=500)

def game_keyPressed(app, event):

    if app.gameState == 1:
        if event.key == 'Space':
            pygame.mixer.Channel(0).play(app.sound1)

        if event.key == 'c':
            pygame.mixer.Channel(1).play(app.sound2)

        if event.key == 'x':
            pygame.mixer.Channel(3).play(app.sound2)

        if event.key == 'z':
            calcGrade(app)
            app.gameState = 2

def addBeats(app):
    if len(app.beatsOnScreen) < 10:
        defualt = 60000/(115*384)

        if app.currBeat in app.beatQ.mainMap:

            if app.beatQ.mainMap[app.currBeat][1] == 'cymb':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'cymb', app.song.getSongTime(), app.song.name,app.avgFPS) )

            elif app.beatQ.mainMap[app.currBeat][1] == 'snare':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'snare', app.song.getSongTime(), app.song.name,app.avgFPS) )

            elif app.beatQ.mainMap[app.currBeat][1] == 'hihat':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'hihat', app.song.getSongTime(), app.song.name,app.avgFPS) )

            elif app.beatQ.mainMap[app.currBeat][1] == 'mid':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'mid', app.song.getSongTime(), app.song.name,app.avgFPS))

            elif app.beatQ.mainMap[app.currBeat][1] == 'high':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'high', app.song.getSongTime(), app.song.name,app.avgFPS) )

            elif app.beatQ.mainMap[app.currBeat][1] == 'floor':
                app.beatsOnScreen.append(DrumKit.createObject(app.beatQ.mainMap[app.currBeat][0], 'floor', app.song.getSongTime(), app.song.name,app.avgFPS) )

        if not (len(app.beatsOnScreen) <= 0) and app.beatsOnScreen[-1] is None:
            app.beatsOnScreen.pop(-1)
        app.currBeat +=1

def updateSongProgress(app):
    app.songProgress = (app.song.getSongTime() / app.song.getSongLength())

def drawScore(app, canvas):
    canvas.create_text(app.width-150, 40, text ='Accuracy: ' + str(int(app.accuracy *100)) + '%', font='Algerian 18 bold')
    canvas.create_text(app.width-150, 300, text ='Score: ' + str(app.score), font='Algerian 18 bold')

def drawCombo(app, canvas):
    canvas.create_text(app.width-150, 800, text ='x' + str(app.combo), font='Algerian 18 bold')

def drawProgressBar(app, canvas):

    x= 550
    y= 50

    xwidth = 600

    canvas.create_rectangle(x, 50, x+xwidth, 75, width = 5)

    xwidth *= app.songProgress
    canvas.create_rectangle(x, 50, x+xwidth, 75, width = 5, fill='black')

def drawStick(app, canvas):
    rad = 10

    try:
        canvas.create_oval(app.redStick[0]-rad, app.redStick[1]-rad, app.redStick[0]+rad, app.redStick[1]+rad, fill='red', width = 3)
        canvas.create_oval(app.blueStick[0]-rad, app.blueStick[1]-rad, app.blueStick[0]+rad, app.blueStick[1]+rad, fill='green', width = 3)
    except:
        pass

def drawGuideCircles(app, canvas):
    #circle guide
    canvas.create_oval(1450-130.9, 333.2-47.59, 1450+130.9, 333.2+47.59, width=10, outline='pink')

    canvas.create_oval(260-130.9, 452.2-47.59, 260+130.9, 452.2+47.59, width=10, outline='purple')


    canvas.create_oval(500-130.9, 833.0-47.59, 500+130.9, 833+47.59, width=10, outline='blue')

    canvas.create_oval(1260-178.5, 797.3-95.19, 1260+178.5, 797.3+95.19, width=10, outline='red')
    canvas.create_oval(1000-130.9, 595-95.19, 1000+130.9, 595+95.19, width=10, outline='green')
    canvas.create_oval(700-130.9, 595.0-95.19, 700+130.9, 595+95.19, width=10, outline='orange')

def drawGameOverScreen(app, canvas):
    canvas.create_text(app.width//2, app.height*(1/9), text='GAME OVER', anchor='center', font='Algerian 50 bold')
    canvas.create_line(300, 200, 1620, 200, width=2)


    scoreText = 'SCORE: ' + str(app.score)
    scoreFontSize = 75
    canvas.create_text(150, 300, text=f'SCORE: {app.score}', anchor='nw', font=f'Algerian {scoreFontSize} ')
    #canvas.create_line(150, 420, len(scoreText)*scoreFontSize-130, 420, width=2)

    hitText = 'HITS/MISSES'
    hitFontSize = 35
    hitx = 200
    canvas.create_text(hitx, 600, text=hitText, anchor='nw', font=f'Algerian {hitFontSize}')
    canvas.create_line(hitx, 660, 525, 660, width=2)
    SubTextFontSize = 20
    canvas.create_text(hitx, 710, text=f"-> Total Hits     {app.hits}x", anchor='nw', font=f'Algerian {SubTextFontSize}')
    canvas.create_text(hitx, 760, text=f"--------> Perfect Hits     {app.perfectHits}x", anchor='nw', font=f'Algerian {SubTextFontSize}')
    canvas.create_text(hitx, 800, text=f"--------> Early Hits         {app.earlyHits}x", anchor='nw', font=f'Algerian {SubTextFontSize}')
    canvas.create_text(hitx, 840, text=f"--------> Late Hits            {app.lateHits}x", anchor='nw', font=f'Algerian {SubTextFontSize}')


    accText = 'Accuracy'
    accFontSize = 35
    canvas.create_text(hitx+660, 630, text=accText, anchor='w', font=f'Algerian {accFontSize}')
    canvas.create_line(hitx+660, 660, hitx+905, 660, width=2)
    acc = 95
    canvas.create_text(hitx+660, 720, text=f"-> {app.accuracy*100}% Hit Rate", anchor='w', font=f'Algerian {SubTextFontSize}')

    comboText = 'COMBO'
    comboFontSize = 35
    canvas.create_text(hitx+660*2, 600, text=comboText, anchor='n', font=f'Algerian {comboFontSize}')
    canvas.create_line(hitx+1245, 660, hitx+1395, 660, width=2)
    canvas.create_text(hitx+1245, 710, text=f"-> Combos     {sum(app.comboDict)}x", anchor='w', font=f'Algerian {SubTextFontSize}')
    canvas.create_text(hitx+1245, 760, text=f"--------> Longest Combo     {app.longestCombo}x", anchor='w', font=f'Algerian {SubTextFontSize}')


    canvas.create_text(hitx+1150, 400, text=f"{app.grade}", anchor='center', font=f'Algerian 300')





    

def game_redrawAll(app, canvas):
    
    if app.gameState == 1:
        if app.isLoading: #allows time for camera, etc to turn on/load
            canvas.create_text(app.width//2, app.height//2, text ='loading' + '.'*app.ellipses, font='Algerian 30 bold')

        elif app.isCountDown:
            canvas.create_text(app.width//2, app.height//2, text =app.countDownNum, font='Algerian 30 bold')
        
        else:
            drawGuideCircles(app, canvas)
            DrumKit.drawObjects(app, canvas)
            drawScore(app, canvas)
            drawCombo(app, canvas)
            drawProgressBar(app, canvas)
            
            drawStick(app, canvas)

    elif app.gameState ==2:
        drawGameOverScreen(app, canvas)
        pass




def game_appStopped(app):
    cv2.destroyAllWindows()
    app.drumstick.capture.release()
    app.song.stop()
    app.camThread.stop()





#MENU =======================================================================================================================
#============================================================================================================================
def menu_mousePressed(app, event):

    
    if app.menuState == 1:
        #play target zone 
        #X: top left (app.buttonX - app.widthRad) --> bot right (app.buttonx + app.widthRad)
        #Y: top left (app.playY - app.heightRad) --> bot right (app.playY + app.heightRad)

        #playgame detector
        if (event.x > (app.buttonX - app.widthRad) and event.x < (app.buttonX + app.widthRad) and
            event.y > (app.playY - app.heightRad) and event.y < (app.playY + app.heightRad)):

            #print(True)
            app.playShadow=False
            app.timerDelay = 1000
            gameStarted(app)

        #score detector
        if (event.x > (app.buttonX - app.widthRad) and event.x < (app.buttonX + app.widthRad) and
            event.y > (app.scoresY - app.heightRad) and event.y < (app.scoresY + app.heightRad)):

            #print(True)
            app.scoreShadow=False
            app.timerDelay = 1000
            app.menuState = 2

        #settings detector
        if (event.x > (app.buttonX - app.widthRad) and event.x < (app.buttonX + app.widthRad) and
            event.y > (app.settingsY - app.heightRad) and event.y < (app.settingsY + app.heightRad)):

            #print(True)
            app.scoreShadow=False
            app.timerDelay = 1000
            app.menuState = 3


    if (event.x > (app.backx - app.backXRad) and event.x < (app.backx + app.backXRad) and
        event.y > (app.backy - app.heightRad) and event.y < (app.backy + app.heightRad)):
        app.scoreShadow=False
        app.timerDelay = 1000
        app.menuState = 1

def menu_timerFired(app):
    app.playShadow=True
    pass

def drawMenuScreen(app, canvas):
    #TODO FIND BACKGROUND
    #font name: groOvEd PERSONAL USE
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#407076')

    canvas.create_text(app.width//2, app.height*(1/9), text='BEAT SMASHER', anchor='center', font='Algerian 80 bold')


    #play button
    if app.playShadow: #'animate' click
        canvas.create_rectangle(app.buttonX-app.widthRad+app.shadowShift, app.playY-app.heightRad+app.shadowShift, app.buttonX+app.widthRad+app.shadowShift, app.playY+app.heightRad+app.shadowShift, fill='black')    
    canvas.create_rectangle(app.buttonX-app.widthRad, app.playY-app.heightRad, app.buttonX+app.widthRad, app.playY+app.heightRad, fill='white', state='disabled') 
    canvas.create_text(app.buttonX, app.playY, text='Play', anchor='center', font='Algerian 30 bold') 

    #scores button
    canvas.create_rectangle(app.buttonX-app.widthRad+app.shadowShift, app.scoresY-app.heightRad+app.shadowShift, app.buttonX+app.widthRad+app.shadowShift, app.scoresY+app.heightRad+app.shadowShift, fill='black')    
    canvas.create_rectangle(app.buttonX-app.widthRad, app.scoresY-app.heightRad, app.buttonX+app.widthRad, app.scoresY+app.heightRad, fill='white') 
    canvas.create_text(app.buttonX, app.scoresY, text='Scores', anchor='center', font='Algerian 30 bold')   
    
    #settings button
    canvas.create_rectangle(app.buttonX-app.widthRad+app.shadowShift, app.settingsY-app.heightRad+app.shadowShift, app.buttonX+app.widthRad+app.shadowShift, app.settingsY+app.heightRad+app.shadowShift, fill='black')    
    canvas.create_rectangle(app.buttonX-app.widthRad, app.settingsY-app.heightRad, app.buttonX+app.widthRad, app.settingsY+app.heightRad, fill='white') 
    canvas.create_text(app.buttonX, app.settingsY, text='Settings', anchor='center', font='Algerian 30 bold')  

def drawScoreScreen(app, canvas):
    canvas.create_text(app.width//2, app.height*(1/9), text='High Scores', anchor='center', font='Algerian 50 bold')
    canvas.create_line(300, 200, 1620, 200, width=2)

    drawBackBtn(app, canvas)

def drawSettingScreen(app, canvas):
    canvas.create_text(app.width//2, app.height*(1/9), text='Settings', anchor='center', font='Algerian 50 bold')
    canvas.create_line(300, 200, 1620, 200, width=2)

    drawBackBtn(app, canvas)

def drawBackBtn(app, canvas):

    canvas.create_rectangle(app.backx-app.backXRad+app.shadowShift, app.backy-app.heightRad+app.shadowShift, app.backx+app.backXRad+app.shadowShift, app.backy+app.heightRad+app.shadowShift, fill='black')    
    canvas.create_rectangle(app.backx-app.backXRad, app.backy-app.heightRad, app.backx+app.backXRad, app.backy+app.heightRad, fill='white') 
    canvas.create_text(app.backx, app.backy, text='Back', anchor='center', font='Algerian 30 bold')  


def menu_redrawAll(app, canvas):
    if app.menuState == 1:

        drawMenuScreen(app, canvas)
    elif app.menuState == 2:
        drawScoreScreen(app, canvas)

    else:
        drawSettingScreen(app, canvas)


def updateTopScores(app, score):

    file = open("TopScores.txt", "w")
    file.write(app.defualtSong +  str(score) + "\n")



#from https://www.tutorialspoint.com/python/python_multithreading.htm#:~:text=Python%20-%20Multithreaded%20Programming%201%20Starting%20a%20New,Synchronizing%20Threads.%20...%205%20Multithreaded%20Priority%20Queue.%20


class camThread(threading.Thread):
    
    def __init__(self, app):
      threading.Thread.__init__(self)
      
      self.running = True
      self.app = app


    def run(self):
        #print ("Starting " + self.name)
        print('running')
        time.sleep(1)

        while self.running:
            self.app.drumstick.run()
            self.app.frame = self.app.drumstick.getFrame()
            self.app.redStick = self.app.drumstick.getRedStickTip()
            self.app.blueStick = self.app.drumstick.getBlueStickTip()

            try:
                #cv2.imshow('f', self.app.drumstick.getFrame())
                pass
            except:
                pass

            if cv2.waitKey(1) == ord('q'):
                break
          
        cv2.destroyAllWindows
        self.app.drumstick.capture.release()

    def stop(self):
        self.running = False
        self.app.drumstick.capture.release()
        cv2.destroyAllWindows

def main():
    #use mvcCheck=False to bypass false mvc violation 
    runApp(width = 1920, height = 1200, mvcCheck=False)

if __name__ == "__main__":
    main()

