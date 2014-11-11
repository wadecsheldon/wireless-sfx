import serial
import effectplayer
import struct
import threading
import time
import random

class instance:

    def __init__(self,filename):
        params = self.load_config(filename)
        self.conn = serial.Serial()
        self.conn.baudrate = params["names"]["baud"]
        self.conn.port = params["names"]["port"] - 1
        self.conn.timeout = params["names"]["timeout"]
        self.conn.open()
        self.effects = []
        self.player = effectplayer.effectplayer()
        for effect in params["keys"].keys():
            self.player.add_effect(effect,params["names"][params["keys"][effect]])
            self.effects.append(effect)
            print "Loaded effect "+effect

    def run(self,interrupt,available_effects,lock):
        while not interrupt.is_set():
            response = self.conn.read(1)
            if len(response) > 0:
                value = struct.unpack('B',response)[0]
                if value == 127 and len(available_effects) > 0:
                    thread = threading.Thread(target=self.play,args=(interrupt, available_effects, lock,))
                    thread.start()
        self.player.stop_all()

    def play(self, interrupt, available_effects, lock):
        lock.acquire()
        effect = random.choice(available_effects)
        available_effects.remove(effect)
        lock.release()
        print effect
        self.player.play_effect(effect)
        time.sleep(.15)
        while self.player.is_playing(effect):
            if interrupt.is_set():
                self.player.stop_effect(effect)
                lock.acquire()
                available_effects.append(effect)
                lock.release()
        self.player.stop_effect(effect)
        lock.acquire()
        available_effects.append(effect)
        lock.release()
        
    def load_config(self,filename):
        fil = open(filename,'r')
        result = {}
        result["names"] = {}
        result["keys"] = {}
        for line in fil.readlines():
            if line != "\n":
                info, data = line.split(":",1)
                dtype = info.split("|")[0]
                name = info.split("|")[1].strip()

                if dtype == "n":
                    result["names"][name] = int(data.strip())
                elif dtype == "s":
                    result["names"][name] = data.lstrip("\t").rstrip("\n")
                elif dtype == "k":
                    result["keys"][name] = data.lstrip("\t").rstrip("\n")
                    

        return result

    def stop(self):
        self.conn.close()

if __name__ == '__main__':
    player = instance("C:\\Python27\\test_config.txt")
    kill = threading.Event()
    lock = threading.RLock()
    effectslist = player.effects
    process = threading.Thread(target=player.run,args=(kill,effectslist,lock,))
    process.start()
    print "Enter to terminate."
    raw_input()
    kill.set()
    player.stop()
    
