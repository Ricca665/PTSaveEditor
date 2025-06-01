import dearpygui.dearpygui as dpg
import configparser
import os
import pymsgbox

config = configparser.ConfigParser()
def OpenRealFileName(saveFileNumber, player, savedatadir):
    global saveFile
    TempsaveFile = ""

    #Decide the save file
    if saveFileNumber == "" or saveFileNumber == "Save file 1":
        TempsaveFile = "saveData1.ini"
    if saveFileNumber == "Save file 2":
        TempsaveFile = "saveData2.ini"
    if saveFileNumber == "Save file 3":
        TempsaveFile = "saveData3.ini"

    #True at the end means that the noise checkbox is checked
    if player:
        TempsaveFile = TempsaveFile.replace(".ini", "")
        TempsaveFile = TempsaveFile + "N.ini"
    saveFile = savedatadir+"/"+TempsaveFile

    try:
        with open(saveFile, "r") as f: # Tries to open the file
            saveFileContents = f.read() # Tries to read the file
        dpg.set_value("file_contents", saveFileContents)
        dpg.show_item("editSaveWindow")
    except Exception: # In case it can't
        pymsgbox.alert("The save file does not exist,\nor a unknown error has occurred", "Error") # Show the error message

    return saveFile

def ReviveSnotty():
    CleanSaveFileGarbage() # Cleans the garbage data at the end
    config.read(saveFile) # Reads the file
    config["Game"]["snotty"] = '"0.000000"'  # Compares each file in the Game section and removes the snotty flag to the games sets the default one

def CleanSaveFileGarbage():
    with open(saveFile, "rb") as f: # opens the file in byte mode
        saveFileData = f.read() # Read the file
        
    #These instruction are REQUIRED since some pizza tower mods, for some reason, add garbage data at 
    #the end of the file, causing this tool to shit itself, this fixes the issue
    saveFileCleanData = saveFileData.replace(b'\00', b'') # Removes those bytes
    with open(saveFile, "wb") as f:
        f.write(saveFileCleanData)

    with open(saveFile, "r") as f:
        saveFileData = f.read()
    
    saveFileCleanData = saveFileData.replace("granny_garbage2N", "utf-8") # This is useless... ESPECIALLY for the Peppino save file
    with open(saveFile, "w") as f:
        f.write(saveFileCleanData)


def SetRanks(level, rank, gerome, secrets):
    CleanSaveFileGarbage()

    config.read(saveFile) # Rereads the save file with configparser, this let's us modify specific sections OF the file

    config["Ranks"][str(level)] = f'"{str(rank)}"'  # Compares each file in the Ranks section of the file and changes it to be a p rank

    if gerome: # In case the gerome box is checked
        config["Treasure"][str(level)] = f'"{str(1.000000)}"'
    else:
        config["Treasure"][str(level)] = f'"{str(0.000000)}"'  

    if secrets > 0: # In case the number of secrets is bigger than 0
        config["Secret"][str(level)] = f'"{str(secrets)}"'
    else:
        config["Secret"][str(level)] = f'"{str(0)}"'

    with open(saveFile, "w") as configfile: # Opens the file
        config.write(configfile) # Writes it back

# dpg.hide_item hides the window
# dpg.show_item shows the window
def showRankScreen():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("rankSetter")

def hideRankScreen():
    dpg.hide_item("rankSetter")
    dpg.show_item("editSaveWindow")

def OpenRAWEditor():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("rawEditor")

def showFriendlyNames(sender, app_data):
    if dpg.is_item_shown("friendly_names"): #In case it's already shown
        dpg.hide_item("friendly_names") # Hide it
    else:
        dpg.show_item("friendly_names") # Show it

def OpenMainScreen():
    save = dpg.get_value("file_contents")
    save = str(save)  # Convert to string
    
    with open(saveFile, "r+") as f: # Writes it
        f.write(save)
        f.truncate()
    
    dpg.hide_item("rawEditor") # Hides the editor
    dpg.show_item("editSaveWindow") # Shows the main menu

def showLHPPEditor():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("lhppSaveEditor")