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
level = "entrance"
secrets = 0
doGerome = False
rank = "p"

dpg.create_context()
dpg.create_viewport(title="PT Save File Editor", width=500, height=500)
dpg.setup_dearpygui()

def _get_player(sender, app_data, user_data):
    global player
    player = app_data
    return player

def _get_savefile_number(sender, app_data, user_data):
    global saveFile
    saveFile = app_data
    return app_data

def _get_level(sender, app_data, user_data):
    global level
    level = app_data
    return level

def _get_secrets(sender, app_data):
    global secrets
    secrets = app_data
    return level

def _get_gerome(sender, app_data):
    global doGerome
    doGerome = app_data
    return doGerome

def _get_rank(sender, app_data):
    global rank
    rank = app_data
    return rank

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
    os.system('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show(\\"The saves folder does not exist,`Please generate it by opening pizza tower, entering a save`and completing the tutorial\\", \\"Error\\", \\"OK\\", \\"Error\\")"') # Show error box
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
    p_rank = dpg.add_button(label="Set rank for level(s)", callback=lambda: showRankScreen())
    cleanshit = dpg.add_button(label="Clean save file ending garbage", callback=lambda: CleanSaveFileGarbage())
    dpg.add_button(label="Manually modify the save", callback=lambda: OpenRAWEditor())

    # Hover tooltips
    with dpg.tooltip(parent=snotty):
        dpg.add_text("Changes the snotty flag to revive")
    with dpg.tooltip(parent=p_rank):
        dpg.add_text("Sets the appropiate flags for each level")
    with dpg.tooltip(parent=cleanshit):
        dpg.add_text("Removes garbage data that is not important\nBut that cause this tool to shit itself\nMods automatically regenerate these bytes")

with dpg.window(tag="rawEditor", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Save and return to main screen", callback=lambda:OpenMainScreen())
    dpg.add_input_text(tag="file_contents", multiline=True, width=700, height=600)
    dpg.set_value("file_contents", saveFile)

with dpg.window(tag="rankSetter", show=False, no_collapse=True, no_close=True, no_title_bar=True, no_move=True):
    dpg.add_button(label="Return to main screen", callback=hideRankScreen)
    dpg.add_combo(label="Level selector", items=["entrance", "medieval", "ruin", "dungeon", "b_pepperman",
                  "badland", "graveyard", "farm", "saloon", "b_noise", "b_vigilante",
                  "b_fakepep", "pizzarush", "trickytreat", "entrway", "exit", "chateau",
                  "kidsparty", "freezer", "street", "industrial", "space", "plage",
                  "forest", "minigolf", "sewer", "war"], callback=_get_level)
    dpg.add_combo(label="Rank to set to", items=["p", "s", "a", "b", "c", "d"], callback=_get_rank)

    dpg.add_slider_int(label="Discovered secrets", min_value=0, max_value= 3, callback=_get_secrets)
    dpg.add_checkbox(label="Gerome treasure", callback=_get_gerome)
    dpg.add_spacer(height=50)
    dpg.add_button(label="Set ranks", callback=lambda:SetRanks(level, rank, doGerome, secrets))

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

#Once at startup
fullscreen_window(None, None, "editSaveWindow")
fullscreen_window(None, None, "rawEditor")
fullscreen_window(None, None, "rankSetter")
dpg.start_dearpygui()

#Destroying when closing
dpg.destroy_context()