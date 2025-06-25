import dearpygui.dearpygui as dpg
import os
import shutil
import sys
import configparser
from utils import *
import errno
import pymsgbox

config = configparser.ConfigParser()
player = False
saveFile = ""
level = "entrance"
secrets = 0
doGerome = False
lunatic = False
rank = "p"
lap = "lap3"
score = 0
keys = False
lapminus = False
laps = "lap 3"
levels = ["entrance", "medieval", "ruin", "dungeon", 
                  "badland", "graveyard", "farm", "saloon",
                   "trickytreat", "entrway", "exit", "chateau",
                  "kidsparty", "freezer", "street", "industrial", "space", "plage",
                  "forest", "minigolf", "sewer", "war"]

bosses = ["b_pepperman", "b_vigilante", "b_noise","b_fakepep"]

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

def _get_lunatic(sender, app_data):
    global lunatic
    lunatic = app_data
    return app_data

def _get_lapping(sender, app_data):
    global lap
    lap = app_data
    return app_data

def _get_score(sender, app_data):
    global score
    score = app_data
    return app_data

def _get_keys(sender, app_data):
    global keys
    keys = app_data
    return app_data

def _get_lapminus(sender, app_data):
    global lapminus
    lapminus = app_data
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
    dpg.add_checkbox(label="Noise", callback=_get_player)
    open_button = dpg.add_button(label="Open file", callback=lambda: OpenRealFileName(saveFile, player, savedatadir))
    with dpg.tooltip(parent=open_button):
        dpg.add_text("Opens the selected save file for editing")

# Main Window
with dpg.window(tag="editSaveWindow", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_text(label="Select actions:")
    snotty = dpg.add_button(label="Revive snotty", callback=lambda: ReviveSnotty())
    p_rank = dpg.add_button(label="Set rank for level(s)", callback=lambda: showRankScreen())
    cleanshit = dpg.add_button(label="Clean save file garbage", callback=lambda: CleanSaveFileGarbage())
    dpg.add_button(label="Manually modify the save", callback=lambda: OpenRAWEditor())
    #lhpp = dpg.add_button(label="Edit LHPP save file", callback=lambda: showLHPPEditor())
    l3dx = dpg.add_button(label="Edit lap 3 deluxe save file", callback=lambda: showL3DXEditor())
    lapminusbutton = dpg.add_button(label="Edit Lap minus save file", callback=lambda: showMinusEditor())
    # Hover tooltips
    #with dpg.tooltip(parent=lhpp):
     #   dpg.add_text("Modify the save files for\nthe Lap Hell: Pizza Pursuit mod")
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
    dpg.add_combo(label="Rank to set to", items=["p", "s", "a", "b", "c", "d"], callback=_get_rank)
    dpg.add_input_float(label="Score", callback=_get_score)
    dpg.add_slider_int(label="Discovered secrets", min_value=0, max_value= 3, callback=_get_secrets)
    dpg.add_checkbox(label="Gerome treasure", callback=_get_gerome)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:SetRanks(level, rank, doGerome, secrets, score))

    friendly_names = dpg.add_button(label="Show friendly names", callback=showFriendlyNames)
    with dpg.tooltip(parent=friendly_names):
        dpg.add_text("Essentially pizza tower references\ninternally the levels as the names in\nthe menu (shown above)\nthis button will show you a list of \nfriendly names in comparison\nto internal pizza tower levels")

with dpg.window(tag="lhppSaveEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)
    
    dpg.add_combo(label="Rank to set to", items=["p", "s"], callback=_get_rank)

    dpg.add_combo(label="Lapping", items=["lap5", "lap4", "lap3"], callback=lambda:_get_lapping)
    dpg.add_checkbox(label="Lunatic mode?", callback=_get_lunatic)
    dpg.add_spacer(height=50)
    #dpg.add_button(label="Set ranks", callback=lambda:lhppSetRanks(level, rank, lunatic, lap))
    friendly_names = dpg.add_button(label="Show friendly names", callback=showFriendlyNames)
    with dpg.tooltip(parent=friendly_names):
        dpg.add_text("Essentially pizza tower references\ninternally the levels as the names in\nthe menu (shown above)\nthis button will show you a list of \nfriendly names in comparison\nto internal pizza tower levels")

with dpg.window(tag="l3dxSaveEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)
    
    dpg.add_combo(label="Rank to set to", items=["p", "s", "a", "b"], callback=_get_rank)
    dpg.add_checkbox(label="Add key?", callback=_get_keys)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:l3dxSetRanks(level, rank, keys))
    friendly_names = dpg.add_button(label="Show friendly names", callback=showFriendlyNames)
    with dpg.tooltip(parent=friendly_names):
        dpg.add_text("Essentially pizza tower references\ninternally the levels as the names in\nthe menu (shown above)\nthis button will show you a list of \nfriendly names in comparison\nto internal pizza tower levels")

with dpg.window(tag="minusSaveWindow", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=levels, callback=_get_level)
    dpg.add_combo(label="Lap", items=["lap 3", "lap 4", "lap 5"], callback=_get_laps)
    dpg.add_combo(label="Rank", items=["p", "s"], callback=_get_rank)
    dpg.add_checkbox(label="Lap minus?", callback=_get_lapminus)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:SetLapMinusRanks(level, rank, lapminus, laps))
    dpg.add_button(label="Unlock CTOP Lapping", callback=lambda:SetCTOPLappingMinusLap())
    friendly_names = dpg.add_button(label="Show friendly names", callback=showFriendlyNames)
    with dpg.tooltip(parent=friendly_names):
        dpg.add_text("Essentially pizza tower references\ninternally the levels as the names in\nthe menu (shown above)\nthis button will show you a list of \nfriendly names in comparison\nto internal pizza tower levels")

with dpg.window(tag="friendly_names", show=False):
    dpg.add_text("entrance = John Gutter")
    dpg.add_text("medieval = Pizzascape")
    dpg.add_text("ruin = Ancient Cheese")
    dpg.add_text("dungeon = Bloodsauce Dungeon")
    dpg.add_text("b_pepperman = Pepperman")
    dpg.add_text("badland = Oregano Desert")
    dpg.add_text("graveyard = Wasteyard")
    dpg.add_text("farm = Fun Farm")
    dpg.add_text("saloon = Fastfood Saloon")
    dpg.add_text("b_vigilante = Vigilante")
    dpg.add_text("plage = Crust Cove")
    dpg.add_text("forest = Gnome Forest")
    dpg.add_text("space = Deep-Dish 9")
    dpg.add_text("minigolf = Golf")
    dpg.add_text("b_noise = Noise")
    dpg.add_text("street = The Pig City")
    dpg.add_text("industrial = Peppibot Factory")
    dpg.add_text("sewer = Oh Shit!")
    dpg.add_text("freezer = Refrigerator-Refrigerador-Freezerator")
    dpg.add_text("b_fakepep = Fake peppino")
    dpg.add_text("chateau = Pizzascare")
    dpg.add_text("kidsparty = Don't Make a Sound")
    dpg.add_text("war = WAR")
    dpg.add_text("exit = The Crumbling Tower of Pizza")

#Finishing initialization
dpg.show_viewport()
dpg.set_primary_window("opensaveFile", True) #Setting it to primary
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "editSaveWindow"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "rankSetter"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "lhppSaveEditor"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "l3dxSaveEditor"))
dpg.set_viewport_resize_callback(lambda s, a: fullscreen_window(s, a, "minusSaveWindow"))

#Once at startup
fullscreen_window(None, None, "editSaveWindow")
fullscreen_window(None, None, "rawEditor")
fullscreen_window(None, None, "rankSetter")
fullscreen_window(None, None, "l3dxSaveEditor")
fullscreen_window(None, None, "minusSaveWindow")

dpg.start_dearpygui()

#Destroying when closing
dpg.destroy_context()
