import time
import os
import sys
import threading

from pyboy import WindowEvent, PyBoy

banner = r"""
  /$$$$$$                                /$$$$$$$                           
 /$$__  $$                              | $$__  $$                          
| $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$ | $$  \ $$  /$$$$$$  /$$   /$$      
| $$  | $$ /$$__  $$ /$$__  $$| $$__  $$| $$$$$$$  /$$__  $$| $$  | $$      
| $$  | $$| $$  \ $$| $$$$$$$$| $$  \ $$| $$__  $$| $$  \ $$| $$  | $$      
| $$  | $$| $$  | $$| $$_____/| $$  | $$| $$  \ $$| $$  | $$| $$  | $$      
|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$| $$$$$$$/|  $$$$$$/|  $$$$$$$      
 \______/ | $$____/  \_______/|__/  |__/|_______/  \______/  \____  $$      
          | $$                                               /$$  | $$      
          | $$                                              |  $$$$$$/      
          |__/                                               \______/       
 Version 0.0.1b
"""

print(banner)

help_msg = """
:BASIC COMMANDS

   COMMAND     DESCRIPTION
   =======     ===========
   help        Shows this message.
   load <ROM>  Specify your ROM file. (Format: *.gb) [ TAKES ARG ]
   launch      Start your Gameboy ROM.

:ADVANCED COMMANDS

   COMMAND                DESCRIPTION
   =======                ===========
   load-savestate <PATH>  Load savestate. [ TAKES ARG ]
   save-savestate <PATH>  Save savestate. [ TAKES ARG ]
"""

class OpenBoy:
    def __init__(self):
        self.pyboy = None
        self.rom = "~"
    def save_progress(self, name:str):
        with open(name, 'wb') as file:
            self.pyboy.save_state(file)
    def load_progress(self, name:str):
        with open(name, 'rb') as file:
            self.pyboy.load_state(file)

def launch(rom:str):
    pyboy = PyBoy(rom)

    while not pyboy.tick():
        pass

    pyboy.stop()

openboy = OpenBoy()

while True:
    cmd = input("OpenBoy (" + openboy.rom + ")> ")
    if cmd == "exit":
        exit()
    if cmd == "help":
        print(help_msg)
    if cmd.startswith("load "):
        try:
            rom = cmd.split(" ")[1]
            if not rom.endswith(".gb"):
                print("[!] Cannot load ROM! Invalid file format.")
                continue
            else:
                print("[*] Loading ROM " + rom + " ...")
                openboy.rom = rom
                print("[+] ROM successfully loaded.")
        except IndexError:
            pass
    if cmd == "launch":
        if openboy.rom == "~":
            print("[!] No ROM was loaded!")
        else:
            def sample():
                openboy.pyboy = PyBoy(openboy.rom)
                while not openboy.pyboy.tick():
                    pass
                openboy.pyboy.stop()
            threading.Thread(target=sample).start()
    if cmd.startswith("load-savestate"):
        try:
            path = cmd.split(" ")[1]
            openboy.load_progress(path)
        except Exception as e:
            print("[~] UNEXPECTED ERROR! " + str(e))
    if cmd.startswith("save-savestate"):
        try:
            path = cmd.split(" ")[1]
            openboy.save_progress(path)
        except Exception as e:
            print("[~] UNEXPECTED ERROR! " + str(e))