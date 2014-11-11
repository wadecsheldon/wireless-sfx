#!/usr/bin/env python
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer
import threading

def dothread(buffage, sond, conn, terminate):
        i = 0
        while i < len(buffage):
            if terminate.is_set():
                break
            if not conn.is_set():
                sond.unpause()
                sond.play(buffage[i])
                i = i+1
            else:
                sond.pause()
        sond.stop()

class effect():

    def __init__(self, fname):
        self.fname = fname
        self.paused = threading.Event()
        self.paused.clear()
        self.kill = threading.Event()
        self.kill.clear()
        self.data = []
        self.snd = None
        self.player = None
        self.load(fname)
        
    def load(self,filename):
        dm = muxer.Demuxer(str.split(filename, '.')[-1].lower())
        f = open(filename, 'rb')
        self.snd = dec = None
        s = f.read( 32000 )
        buff = []
        while len(s):
            frames = dm.parse(s)
            if frames:
                for fr in frames:
                    if dec == None:
                        dec = acodec.Decoder(dm.streams[fr[0]])

                    r = dec.decode(fr[1])
                    if r and r.data:
                        if self.snd == None:
                            self.snd = sound.Output(
                                int(r.sample_rate),
                                r.channels,
                                sound.AFMT_S16_LE)
                        self.data.append(r.data)
            s = f.read(512)

    def play(self):
        if self.player == None:
            self.kill.clear()
            self.paused.clear()
            self.player = threading.Thread(target=dothread, args=(self.data,self.snd,self.paused,self.kill,))
            self.player.start()
        else:
            self.paused.clear()

    def stop(self):
        if self.player != None:
            self.kill.set()
            self.player = None

    def pause(self):
        self.paused.set()

    def is_active(self):
        if self.player != None:
            return self.player.is_alive()
        else:
            return False
            

class effectplayer():

    def __init__(self):
        self.effects = {}

    def add_effect(self,name,filename):
        self.effects[name] = effect(filename)

    def play_effect(self,name):
        self.effects[name].play()

    def pause_effect(self,name):
        self.effects[name].pause()

    def stop_effect(self,name):
        self.effects[name].stop()

    def is_playing(self,name):
        return self.effects[name].is_active()

    def stop_all(self):
        for name in self.effects.keys():
            self.effects[name].stop()
        
