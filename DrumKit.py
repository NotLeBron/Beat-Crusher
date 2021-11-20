from cmu_112_graphics import *

class DrumPiece(object):

    def __init__(self, timeStamp, scale):

        self.timeStamp = timeStamp

        self.scale = scale


        self.isActive

    def isActive(self):
        return self.isActive


    def getTimeStamp(self):
        return self.timeStamp


    def scaleObject(self, scale):
        self.scale = scale

    def drawObject(self, canvas):

        pass


class Snare(DrumPiece):

    def __init__(self, timeStamp, scale):
        super().__init__(timeStamp, scale)

    
    def drawObject(self, canvas):
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

    def __init__(self, timeStamp, scale, type):
        super().__init__(timeStamp, scale)

        self.type = type

    def drawObject(self, canvas):
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

    def __init__(self, timeStamp, scale):
        super().__init__(timeStamp, scale)

    def drawObject(self, canvas):
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

    def __init__(self, timeStamp, scale):
        super().__init__(timeStamp, scale)

    def drawObject(self, canvas):

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


    


    
    
    







def appStarted(app):
    app.scale  = .01
    #.img = Image.open('background.png')

    app.snare = Snare(1, app.scale)
    app.hihat = HiHat(1, app.scale)
    app.midTom = Tom(1, app.scale, 'mid')
    app.highTom = Tom(1, app.scale, 'high')
    app.floorTom = Tom(1, app.scale, 'floor')
    app.crashCymbol = CrashCymbol(1, app.scale)

    app.drumKit = set()
    app.drumKit.add(app.snare)
    app.drumKit.add(app.hihat)
    app.drumKit.add(app.midTom)
    app.drumKit.add(app.highTom)
    app.drumKit.add(app.floorTom)
    app.drumKit.add(app.crashCymbol)


def keyPressed(app, event):

    if event.key == 'Up':
        app.scale  += .05

        for object in app.drumKit:
            object.scaleObject(app.scale)

    if event.key == 'Down':
        if not app.scale  - .05 < 0:
            app.scale  -= .05

            for object in app.drumKit:
                object.scaleObject(app.scale)

    if app.scale  > 1.19:
        app.scale  = 1.19
        for object in app.drumKit:
            object.scaleObject(app.scale)

def timerFired(app):

    #.scale += .1

    if app.scale  > 1.19:
        app.scale  = 1.19

def redrawAll(app, canvas):

    #canvas.create_image(.width / 2, (.height / 2)-40, image=ImageTk.PhotoImage(.img))

    canvas.create_rectangle(0,0, app.width, app.height, fill='GRAY')

    #OBJECTS===============================
    for object in app.drumKit:
            object.drawObject(canvas)


    #======================================
    #circle guide
    canvas.create_oval(1450+130.9, 333.2+47.59, 1450-130.9, 333.2-47.59, width=10, outline='pink')

    canvas.create_oval(260+130.9, 452.2+47.59, 260-130.9, 452.2-47.59, width=10, outline='purple')

    canvas.create_oval(260+130.9, 452.2+47.59, 260-130.9, 452.2-47.59, width=10, outline='purple')

    canvas.create_oval(500+130.9, 833.0+47.59, 500-130.9, 833-47.59, width=10, outline='#DEE5E5')

    canvas.create_oval(1260+178.5, 797.3+95.19, 1260-178.5, 797.3-95.19, width=10, outline='#DEE5E5')
    canvas.create_oval(1000+130.9, 595+95.19, 1000-130.9, 595-95.19, width=10, outline='#DEE5E5')
    canvas.create_oval(700+130.9, 595.0+95.19, 700-130.9, 595-95.19, width=10, outline='#DEE5E5')

    pass


def main():
    runApp(width = 1920, height = 1200)

if __name__ == "__main__":
    main()
