import pygame, pyaudio, wave, time 
from threading import Thread
import queue
from cmu_112_graphics import *


pygame.mixer.init()


class DrumAudioHandler(object):

    def __init__(self, app):
        pygame.mixer.init()

        self.snare = pygame.mixer.Sound('Resources/Audio files/snare.mp3')
        self.hihat = pygame.mixer.Sound('Resources/Audio files/hihat.mp3')
        self.midTom = pygame.mixer.Sound('Resources/Audio files/midTom.mp3')
        self.highTom = pygame.mixer.Sound('Resources/Audio files/highTom.mp3')
        self.floorTom = pygame.mixer.Sound('Resources/Audio files/floorTom.mp3')
        self.cymb = pygame.mixer.Sound('Resources/Audio files/cymb.mp3')
        self.kick = pygame.mixer.Sound('Resources/Audio files/kick.mp3')

        self.maxThreads = 30
        self.workList = []

        self.q = queue.Queue()
        self.threads = []

        self.threadInit()

    def threadInit(self):
        for i in range(self.maxThreads):
            t = Thread(target=self.worker)
            t.name = f'Audio Thread {i}'
            t.setDaemon(True)
            t.start()
            self.threads.append(t)

    def playCymb(self):
        self.cymb.play()
        return

    def playSnare(self):
        self.snare.play(maxtime=100)
        return

    def playHihat(self):
        self.hihat.play()
        return

    def playMidTom(self):
        self.midTom.play()
        return

    def playHighTom(self):
        self.highTom.play()
        return

    def playFloorTom(self):
        self.floorTom.play()
        return

    def playKick(self):
        self.kick.play()

    def worker(self):
        #Help from python queue & multithreadingexample https://gist.github.com/arthuralvim/356795612606326f08d99c6cd375f796
        while True:
            item = self.q.get()
            if item is None:
                break
            item()
            try:
                self.workList.remove(item)
            except:
                pass
            self.q.task_done()

    def addWork(self, piece):

        if piece == 'snare':

            self.workList.append(self.playSnare)

        elif piece == 'hihat':
            self.workList.append(self.playHihat)

        elif piece == 'mid':
            self.workList.append(self.playMidTom)

        elif piece == 'high':
            self.workList.append(self.playHighTom)

        elif piece == 'floor':
            self.workList.append(self.playFloorTom)

        elif piece == 'cymb':
            self.workList.append(self.playCymb)

        elif piece == 'kick':
            self.workList.append(self.playKick)

    def executeWork(self, app):
        for item in self.workList:
            self.q.put(item)

        self.q.join()




