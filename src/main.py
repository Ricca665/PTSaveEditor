import dearpygui.dearpygui as dpg #Dear py gui my beloved
import requests
import os
import shutil
import sys
import configparser
from utils import *
import errno
import pymsgbox
currversiontag = "newcrashmenu"
githubdownloads = ""

config = configparser.ConfigParser()
player = False
saveFile = ""
level = "John gutter"
secrets = 0
doGerome = False
rank = "p"
lap = "lap3"
score = 0
keys = False
lapminus = False
isLunaticMode = False
isSwapMode = False
laps = "lap 3"

# Duplicate list, one with internally referenced games and another one with the friendly names
internal_levels = ["entrance", "medieval", "ruin", "dungeon", 
                  "badland", "graveyard", "farm", "saloon",
                   "exit", "chateau", "kidsparty", "freezer", 
                   "street", "industrial", "space", "plage",
                  "forest", "minigolf", "sewer", "war"]

levels = ["John gutter", "Pizzascape", "Ancient Cheese", "Bloodsauce Dungeon", 
                  "Oregano Desert", "Wasteyard", "Fun Farm", "Fastfood Saloon",
                   "Crust Cove", "Gnome Forest", "Deep-Dish 9", "GOLF", 
                   "The Pig City", "Peppibot Factory", "Oh Shit!", "RRF", 
                   "Pizzascare", "DMAS", "WAR", "CTOP"]

bosses = ["Pepperman", "Vigilante", "Noise","Fake peppino"]

internal_bosses = ["b_pepperman", "b_vigilante", "b_noise","b_fakepep"]


ranks = ["p", "s", "a", "b", "c", "d"]
normal_lap3ranks = ["p", "s"]

dpg.create_context()
dpg.create_viewport(title="PT Save File Editor", width=500, height=500)
dpg.setup_dearpygui()

def _get_player(sender, app_data, user_data):
    global player
    player = app_data
    return app_data

def _get_savefile_number(sender, app_data, user_data):
    global saveFile
    saveFile = app_data
    return app_data

def _get_level(sender, app_data, user_data):
    global level
    level = app_data
    return app_data

def _get_secrets(sender, app_data):
    global secrets
    secrets = app_data
    return app_data

def _get_gerome(sender, app_data):
    global doGerome
    doGerome = app_data
    return app_data

def _get_rank(sender, app_data):
    global rank
    rank = app_data
    return app_data

def _get_lunaticmode(sender, app_data):
    global isLunaticMode
    isLunaticMode = app_data
    return app_data

def _get_score(sender, app_data):
    global score
    score = app_data
    return app_data

def _get_keys(sender, app_data):
    global keys
    keys = app_data
    return app_data

def _get_swapmode(sender, app_data):
    global isSwapMode
    isSwapMode = app_data
    return app_data

def _get_lapminus(sender, app_data):
    global lapminus
    lapminus = app_data
    if lapminus: # if lap minus is toggled
        dpg.configure_item("lapselector4lapminus", items=["lap 2", "lap 3", "lap 4", "lap 5"]) # dynamically change the lap selector
    else:
        dpg.configure_item("lapselector4lapminus", items=["lap 3", "lap 4", "lap 5"]) # dynamically change the lap selector
    return app_data

def _get_laps(sender, app_data):
    global laps
    laps = app_data
    return app_data

def fullscreen_window(sender, app_data, user_data):
    width, height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
    dpg.set_item_width(user_data, width)
    dpg.set_item_height(user_data, height)
    dpg.set_item_pos(user_data, (0, 0))  # Top-left corner

# auto check for updates
import json
currversiontag = "s"
try:
    isinternet = requests.get("https://api.github.com").status_code == 200
except:
    isinternet = False

if isinternet:
    request = requests.get("https://api.github.com/repos/Ricca665/PTSaveEditor/releases/latest")
    x = json.dumps(request.json())
    y = json.loads(x)
    tag_name = y["tag_name"]

    if tag_name == currversiontag:
        print("Up to date!")
    else:
        print(f"A new version is avaible! {tag_name}")
        print("Do you want to download it?")
        didnotinput = True
        while didnotinput:
            answer = input("Y/n")
            if answer.lower() == "y":
                print("Downloading!")
                didnotinput = False
                break
            elif answer.lower() == "n":
                print("ok")
                didnotinput = False
                break
        if answer.lower() == "y":
            requests.get("google.com")

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
            pass  # WINDOWS, I DON'T GIVE A GODDAMN FUCKING SHIT ABOUT THE DIRECTORY EXISTING, GET GET GET OUT! 
   
    saves = os.listdir()

except Exception as e:
    # The following line basically tells it to create a error popup window
    pymsgbox.alert(f"""The saves folder does not exist or an unknown error has occured.\n
                   Please generate it by opening pizza tower, entering a save\nand
                   completing the tutorial\nTrace:\n{e}""", "An error has occured!")
    sys.exit(1) # Exit

#We initialize the buttons and other stuff
#Tag means how internally it references itself
#Show means to not show it at startup
#No collapse means don't show the collapse button
#No close means don't show the close button
#No title bar means to not show the titlebar
#No move means that you can't move the window 

with dpg.window(tag="opensaveFile"):
    dpg.add_text("Select your save file: ")
    dpg.add_radio_button(("Save file 1", "Save file 2", "Save file 3"), callback=_get_savefile_number, horizontal=True)
    dpg.add_checkbox(label="Is Noise Save File?", callback=_get_player)
    swap_mode = dpg.add_checkbox(label="Is Swap Mode?", callback=_get_swapmode)
    open_button = dpg.add_button(label="Open file", callback=lambda: OpenRealFileName(saveFile, player, savedatadir))
    with dpg.tooltip(parent=open_button):
        dpg.add_text("Opens the selected save file for editing")
    with dpg.tooltip(parent=swap_mode):
        dpg.add_text("Only used by Lap Hell: Pizza pursuit")

# Main Window
with dpg.window(tag="editSaveWindow", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_text(label="Select actions:")
    snotty = dpg.add_button(label="Revive snotty", callback=lambda: ReviveSnotty())
    p_rank = dpg.add_button(label="Set rank for level(s)", callback=lambda: showRankScreen())
    cleanshit = dpg.add_button(label="Clean save file garbage", callback=lambda: CleanSaveFileGarbage())
    dpg.add_button(label="Manually modify the save", callback=lambda: OpenRAWEditor())
    l3dx = dpg.add_button(label="Edit lap 3 deluxe save file", callback=lambda: showL3DXEditor())
    lapminusbutton = dpg.add_button(label="Edit Lap minus save file", callback=lambda: showMinusEditor())
    lhpp = dpg.add_button(label="Edit Lap hell: Pizza pursuit save file", callback=lambda: showLHPPEditor())
    # Hover tooltips
    with dpg.tooltip(parent=snotty):
        dpg.add_text("Changes the snotty flag to revive him")
    with dpg.tooltip(parent=p_rank):
        dpg.add_text("Sets the appropiate ranks (and other) for each level")
    with dpg.tooltip(parent=cleanshit):
        dpg.add_text("Removes garbage data that is not important\nBut that cause this tool to not work.\nMods automatically regenerates this data")


with dpg.window(tag="rawEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Save and return to main screen", callback=lambda:OpenMainScreen())
    dpg.add_input_text(tag="file_contents", multiline=True, width=700, height=600)
    saveFileContents = config.read(saveFile)
    dpg.set_value("file_contents", saveFileContents)

with dpg.window(tag="rankSetter", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels+bosses, callback=_get_level)
    dpg.add_combo(label="Rank to set to", items=ranks, callback=_get_rank)
    dpg.add_input_float(label="Score", callback=_get_score)
    dpg.add_slider_int(label="Discovered secrets", min_value=0, max_value= 3, callback=_get_secrets)
    dpg.add_checkbox(label="Gerome treasure", callback=_get_gerome)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:SetRanks(level, rank, doGerome, secrets, score))

with dpg.window(tag="l3dxSaveEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)

    dpg.add_combo(label="Rank to set to", items=["p", "s", "a", "b"], callback=_get_rank)
    dpg.add_checkbox(label="Add key?", callback=_get_keys)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:l3dxSetRanks(level, rank, keys))
    
with dpg.window(tag="lhppSaveEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)

    dpg.add_combo(label="Lap", items=["lap 3", "lap 4", "lap 5"], callback=_get_laps, tag="lapselector4lhpp")
    dpg.add_combo(label="Rank", items=normal_lap3ranks, callback=_get_rank, tag="rankselector4lhpp")

    dpg.add_checkbox(label="Lunatic mode?", callback=_get_lunaticmode)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:lhppSetRanks(level, rank, laps, isLunaticMode, player, isSwapMode))


with dpg.window(tag="minusSaveWindow", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)
    dpg.add_combo(label="Lap", items=["lap 3", "lap 4", "lap 5"], callback=_get_laps, tag="lapselector4lapminus")
    dpg.add_combo(label="Rank", items=normal_lap3ranks, callback=_get_rank, tag="rankselector4lapminus")

    dpg.add_checkbox(label="Lap minus?", callback=_get_lapminus)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:SetLapMinusRanks(level, rank, lapminus, laps))
    dpg.add_button(label="Unlock CTOP Lapping", callback=lambda:SetCTOPLappingMinusLap())

#Finishing initialization
dpg.show_viewport()
dpg.set_primary_window("opensaveFile", True) #Setting it to primary
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "rankSetter"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "l3dxSaveEditor"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "minusSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "lhppSaveEditor"))

#Once at startup
fullscreen_window(None, None, "editSaveWindow")
fullscreen_window(None, None, "rawEditor")
fullscreen_window(None, None, "rankSetter")
fullscreen_window(None, None, "l3dxSaveEditor")
fullscreen_window(None, None, "minusSaveWindow")
fullscreen_window(None, None, "lhppSaveEditor")

dpg.start_dearpygui()

#Destroying when closing
dpg.destroy_context()
