import dearpygui.dearpygui as dpg
import os
import shutil
import sys
import configparser
from utils import *
import errno

config = configparser.ConfigParser()
player = False
saveFile = ""
dpg.create_context()
dpg.create_viewport(title="PT Save File Editor", width=750, height=700)
dpg.setup_dearpygui()

def _get_player(sender, app_data, user_data):
    global player
    player = app_data
    return player

def _get_savefile_number(sender, app_data, user_data):
    global saveFile
    saveFile = app_data
    return app_data

def fullscreen_window(sender, app_data, user_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width(user_data, width)
    dpg.set_item_height(user_data, height)
    dpg.set_item_pos(user_data, (0, 0))  # Top-left corner

try:
    appdata_dir = os.environ['APPDATA'].replace("\\", "/")
    savedatadir = appdata_dir + "/PizzaTower_GM2/saves"
    currentdir = os.getcwd().replace("\\", "/")
    backupdir = currentdir+"/backup"
    try:
        os.makedirs(backupdir)
        os.chdir(savedatadir)
        shutil.copytree(savedatadir, backupdir, dirs_exist_ok=True)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass  # WINDOWS, I DON'T GIVE A GODDAMN FUCKING SHIT ABOUT THE DIRECTORY EXISTING, GET OUT!
   
    saves = os.listdir()

except Exception as e:
    #os.system('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show(\\"The saves folder does not exist,`Please generate it by opening pizza tower, entering a save`and completing the tutorial\\", \\"Error\\", \\"OK\\", \\"Error\\")"') # Show error box
    print(e)
    sys.exit(1)

#We initialize the buttons and other stuff
with dpg.window(tag="opensaveFile"):
    dpg.add_text("Select your save file: ")
    dpg.add_radio_button(("Save file 1", "Save file 2", "Save file 3"), callback=_get_savefile_number, horizontal=True)
    dpg.add_checkbox(label="Noise", callback=_get_player)
    open_button = dpg.add_button(label="Open file", callback=lambda: OpenRealFileName(saveFile, player, savedatadir))
    with dpg.tooltip(parent=open_button):
        dpg.add_text("Opens the selected save file for editing")

with dpg.window(tag="editSaveWindow", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_text(label="Select actions:")
    snotty = dpg.add_button(label="Revive snotty", callback=lambda: ReviveSnotty())
    p_rank = dpg.add_button(label="Get P Rank in every level", callback=lambda: GetPRank())
    cleanshit = dpg.add_button(label="Clean save file ending garbage", callback=lambda: CleanSaveFileGarbage())
    dpg.add_button(label="Manually modify the save", callback=lambda: OpenRAWEditor())

    # Hover tooltips
    with dpg.tooltip(parent=snotty):
        dpg.add_text("Changes the snotty flag to revive")
    with dpg.tooltip(parent=p_rank):
        dpg.add_text("Sets the p rank flag for every level")
    with dpg.tooltip(parent=cleanshit):
        dpg.add_text("Removes garbage data that is not important\nBut that cause this tool to shit itself\nMods automatically regenerate these bytes")

with dpg.window(tag="rawEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Save and return to main screen", callback=lambda:OpenMainScreen())
    dpg.add_input_text(tag="file_contents", multiline=True, width=700, height=600)
    dpg.set_value("file_contents", saveFile)


#Finishing initialization
dpg.show_viewport()
dpg.set_primary_window("opensaveFile", True) #Setting it to primary
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))

#Once at startup
fullscreen_window(None, None, "editSaveWindow")
fullscreen_window(None, None, "rawEditor")
dpg.start_dearpygui()

#Destroying when closing
dpg.destroy_context()