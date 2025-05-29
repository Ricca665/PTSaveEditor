import dearpygui.dearpygui as dpg
import os
import time
import sys
import configparser
from utils import *

config = configparser.ConfigParser()
player = ""
saveFile = ""
dpg.create_context()
dpg.create_viewport(title="YA ADB/Fastboot GUI", width=750, height=700)
dpg.setup_dearpygui()

def _get_player(sender, app_data, user_data):
    global player
    player = app_data
    return player

def _get_savefile_number(sender, app_data, user_data):
    global saveFile
    saveFile = app_data
    return saveFile

try:
    appdata_dir = os.environ['APPDATA'].replace("\\", "/")
    savedatadir = appdata_dir + "/PizzaTower_GM2/saves"
    os.chdir(savedatadir)
    saves = os.listdir()
    if not "saveData" in saves:
        raise Exception
except:
    print("You don't seem to have a valid pizza tower save file...")

#We initialize the buttons and other stuff
with dpg.window(tag="primary"):
    dpg.add_text("Select your save file: ")
    dpg.add_radio_button(("Save file 1", "Save file 2", "Save file 3"), callback=_get_savefile_number, horizontal=True)
    dpg.add_radio_button(("Peppino", "Noise"), callback=_get_player, horizontal=True)
    dpg.add_button(label="Open file", callback=lambda: OpenRealFileName(_get_savefile_number, _get_player))


#Finishing initialization by viewing our window
dpg.show_viewport()
dpg.set_primary_window("primary", True) #Setting it to primary
dpg.start_dearpygui()

#Destroying when closing
dpg.destroy_context()