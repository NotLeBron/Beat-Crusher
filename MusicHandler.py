import pygame


class Song(object):
    """Purpose: plays main song and keeps track of important song infor (song length, pos, etc)"""
    def __init__(self, name):
        #https://people.csail.mit.edu/hubert/pyaudio/docs/ example used

        pygame.mixer.init()

        self.name = name
        self.playing = False

        if self.name == 'Smells Like Teen Spirit':
            pygame.mixer.music.load('Resources/Songs/Smells Like Teen Spirit.wav')
            self.bpm = 117
            self.offset = 0
            self.ppq = 384
            self.tickPerSecond = 60000/(self.bpm*self.ppq)
            self.songPosition = 0 #changes one song starts
            self.playing = True

        elif self.name == 'Boulevard of Broken Dreams':
            pygame.mixer.music.load('Resources/Songs/Boulevard of Broken Dreams.wav')
            self.bpm = 83
            self.offset = 0
            self.ppq = 480
            self.tickPerSecond = 60000/(self.bpm*self.ppq)
            self.songPosition = 0 #changes one song starts
            self.playing = True


        else:
            self.bpm = None
            raise Exception('Song Doesn\'t Exist')

        pygame.mixer.music.set_volume(.7)

    def updateSongPosition(self, newPos):
        self.songPosition = newPos

    def getTicksPerSec(self):
        return self.tickPerSecond

    def getSongTime(self):

        return pygame.mixer.music.get_pos() / 1000


    def play(self):
        pygame.mixer.music.play(0)

    def stop(self):
        pygame.mixer.music.stop()


    def getSongLength(self):
        if self.name == 'Smells Like Teen Spirit':
            temp = pygame.mixer.Sound('Resources/Songs/Smells like Teen Spirit.wav')

        elif self.name == 'Boulevard of Broken Dreams':
            temp = pygame.mixer.Sound('Resources/Songs/Boulevard of Broken Dreams.wav')
        return temp.get_length()

class BeatQueue(object):
    """purpose: read in a midi txt file and create a beatmap that this program can use"""
    def __init__(self, song, track):
        self.song = song
        self.filepath = 'Resources/BeatMaps/'

        self.mainMap, self.kickBeatMap = self.parsebeatmap(self.filepath+song+'.txt', track)
        


    def getBeat(self, beatId):
        """removes and returns a beat if it matches the given beatID"""

        for set in self.beatmap:
            if beatId in set:
                return self.beatmap

        return self.beatmap.pop(beatId, None)


    def parsebeatmap(self, filepath, track):
        """parses a beat map text file"""

        beatMap = dict()

        kickBeats = [] #for bass drum

        beatID = 0 #place of beat in queue

        #organize Data
        with open(filepath) as beats:
            for  index, line in enumerate(beats):
                line = line.strip() 
                
                splitLine = line.split(', ')

                if int(splitLine[0]) == track:
                    #assigns each beats its respective drum piece

                    if int(splitLine[4]) == 38:

                        beatMap[beatID] = (int(splitLine[1]), 'snare')

                    elif int(splitLine[4]) == 42:
                        beatMap[beatID] = (int(splitLine[1]), 'hihat')

                    elif int(splitLine[4]) == 43:
                        beatMap[beatID] = (int(splitLine[1]), 'floor')

                    elif int(splitLine[4]) == 47:
                        beatMap[beatID] = (int(splitLine[1]), 'mid')

                    elif int(splitLine[4]) == 48:
                        beatMap[beatID] = (int(splitLine[1]), 'high')

                    elif int(splitLine[4]) == 49:
                        beatMap[beatID] = (int(splitLine[1]), 'cymb')

                    elif int(splitLine[4]) == 36:
                        kickBeats.append((int(splitLine[1]), 'kick'))

                    
                    beatID += 1

                    
        return beatMap, kickBeats
    

#debugging purposes  
def printDict(dict):

    for element in dict:
        print(str(element) + ": " + str(dict[element]))



class songInfo():
    """holds vital info on each songs"""


    def getTickPerSecond(song):
        # https://stackoverflow.com/questions/2038313/converting-midi-ticks-to-actual-playback-seconds
        #formula for midi ticks to seconds
        if song =='Smells Like Teen Spirit':
            bpm = 116
            offset = 0
            ppq = 384
            return  60000/(bpm*ppq)


        elif song =='Boulevard of Broken Dreams':
            bpm = 83
            offset = 0
            ppq = 480


    def getTotalBeats(song):
        if song =='Smells Like Teen Spirit':
            return 1727


        elif song =='Boulevard of Broken Dreams':
            return 1221
