import dearpygui.dearpygui as dpg
import configparser
import re
import pymsgbox
import sys

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

    with open(saveFile, "w") as configfile: # Opens the file
        config.write(configfile) # Writes it back

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
       
    saveFileCleanData = saveFileData
    # Some noise shit
    saveFileCleanData = saveFileCleanData.replace('granny_garbage2N="0.000000"', "")
    saveFileCleanData = saveFileCleanData.replace('granny_forest1N="0.000000"', "")
    saveFileCleanData = saveFileCleanData.replace('granny_hubtips7N="0.000000"', "")
    saveFileCleanData = saveFileCleanData.replace('granny_garbage7N="0.000000"', "")
    saveFileCleanData = saveFileCleanData.replace('granny_garbage1N="0.000000"', "")
    saveFileCleanData = saveFileCleanData.replace('granny_garbage5N="0.000000"', "")
    
    # Some of my mess
    # In previous versions of the tool because of the replace shenanigans
    # Above me, it deleted part of the string
    # This removes that
    saveFileCleanData = re.sub(r'(?m)^\s*="0\s*\n?', '', saveFileCleanData)
    saveFileCleanData = re.sub(r'(?m)^\s*.000000"\s*\n?', '', saveFileCleanData)

    # So basically lap 3 deluxe is very intelligent, if you get catched more than one time by QnVybnRmYWNl
    # It writes it n times you have been catched
    # This just adds ONE of it
    l3dxstring = "l3dxqnvybnrmywnl"
    saveFileLines = saveFileCleanData.splitlines()
    didFindString = False
    for i in saveFileLines:
        if l3dxstring in i:
            if not didFindString:
                didFindString = True
                saveFileCleanData = saveFileCleanData.replace(i, "")
    # need to fix this, it places it in the wrong line :/

    with open(saveFile, "w") as f:
        f.write(saveFileCleanData)

def l3dxSetRanks(level, rank, keys):
    CleanSaveFileGarbage()
    config.read(saveFile)

    if "Lapped3" not in config:
        config["Lapped3"] = {}
    
    if "3Rank" not in config:
        config["3Rank"] = {}
    
    if "LapKey" not in config:
        config["LapKey"] = {}

    level = str(level)+"6" # L3DX saves the data for each level as level+6 and then the value
                           # By doing this we are doing it just once
                           # SO if the level was "entrance" it would be entrance6

    config["Lapped3"][level] = f'"2.000000"'
    config["3Rank"][level] = f'"{rank}"' # Rank

    if keys:
        config["LapKey"][level] = f'"1.000000"' # The keys for each level are saved separately
    else:
        config["LapKey"][level] = f'"0.000000"'

    with open(saveFile, "w") as configfile: # Opens the file
        config.write(configfile) # Writes it back

def SetRanks(level, rank, gerome, secrets, score):
    CleanSaveFileGarbage()

    config.read(saveFile) # Rereads the save file with configparser, this let's us modify specific sections OF the file
    
    if "Ranks" not in config:
        config["Ranks"] = {}
        
    config["Ranks"][str(level)] = f'"{str(rank)}"'  # Compares each file in the Ranks section of the file and changes it to be a p rank

    if "Treasure" not in config:
        config["Treasure"] = {}

    if gerome: # In case the gerome box is checked
        config["Treasure"][str(level)] = f'"{str(1.000000)}"'
    else:
        config["Treasure"][str(level)] = f'"{str(0.000000)}"'  

    if "Secret" not in config:
        config["Secret"] = {}

    if secrets > 0: # In case the number of secrets is bigger than 0
        config["Secret"][str(level)] = f'"{str(secrets)}"'
    else:
        config["Secret"][str(level)] = f'"{str(0)}"'

    if "Highscore" not in config:
        config["Highscore"] = {}

    if score > 0:
        config["Highscore"][str(level)] = f'"{str(score)}"'

    with open(saveFile, "w") as configfile: # Opens the file
        config.write(configfile) # Writes it back

def lhppSetRanks(level, rank, lunatic, lapping):
    CleanSaveFileGarbage()

    config.read(saveFile) # Rereads the save file with configparser, this let's us modify specific sections OF the file

    #config["Ranks"][str(level)] = f'"{str(rank)}"'  # Compares each file in the Ranks section of the file and changes it to be a p rank

def SetLapMinusRanks(level, rank, islapminus, lap):
    
    CleanSaveFileGarbage()

    config.read(saveFile) # Reads the file

    if "LapMinusNegative" not in config:
        config["LapMinusNegative"] = {}

    
    if "LapMinusPositive" not in config:
        config["LapMinusPositive"] = {}

    # This is the lapping table for the Lap minus mod:
    # For the lap minus (so lap -3, -4 and -5):
    # NUMBER | LAP NUMBER | MEANING
    # 7            5        Lap 5 P Rank
    # 6            5        Lap 5 S Rank
    # 5            4        Lap 4 P Rank
    # 4            4        Lap 4 S Rank 
    # 3            3        Lap 3 P Rank
    # 2            3        Lap 3 S Rank 
    #    Maybe something for Lap 2?
    # For the normal lapping (so lap 3, 4 and 5):
    # NUMBER | LAP NUMBER | MEANING
    # 6            5        Lap 5 P Rank
    # 5            5        Lap 5 S Rank
    # 4            4        Lap 4 P Rank
    # 3            4        Lap 4 S Rank 
    # 2            3        Lap 3 P Rank
    # 1            3        Lap 3 S Rank 

    # Behold, THE... uhh... lap checker shit
    # HELL YEAH!!!!
    # TODO (hopefully) fix this mess (maybe make a number and subtract it?)


    if islapminus:
        if lap == "lap 5":
            if rank == "p":
                config["LapMinusNegative"][str(level)] = f'"{str(7)}"'
            else:
                config["LapMinusNegative"][str(level)] = f'"{str(6)}"'
        elif lap == "lap 4":
            if rank == "p":
                config["LapMinusNegative"][str(level)] = f'"{str(5)}"'
            else:
                config["LapMinusNegative"][str(level)] = f'"{str(4)}"'
        elif lap == "lap 3":
            if rank == "p":
                config["LapMinusNegative"][str(level)] = f'"{str(3)}"'
            elif rank == "s":
                config["LapMinusNegative"][str(level)] = f'"{str(2)}"'
    else:
        if lap == "lap 5":
            if rank == "p":
                config["LapMinusPositive"][str(level)] = f'"{str(6)}"'
            else:
                config["LapMinusPositive"][str(level)] = f'"{str(5)}"'
        elif lap == "lap 4":
            if rank == "p":
                config["LapMinusPositive"][str(level)] = f'"{str(4)}"'
            else:
                config["LapMinusPositive"][str(level)] = f'"{str(3)}"'
        elif lap == "lap 3":
            if rank == "p":
                config["LapMinusPositive"][str(level)] = f'"{str(2)}"'
            else:
                config["LapMinusPositive"][str(level)] = f'"{str(1)}"'
        
    with open(saveFile, "w") as configfile: # Opens the file
        config.write(configfile) # Writes it back

def SetCTOPLappingMinusLap():
    CleanSaveFileGarbage()

    config.read(saveFile)

    if "Unlocks" not in config:
        config["Unlocks"] = {}
    
    config["Unlocks"]["minus_tctop"] = f'"1"'

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

def showL3DXEditor():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("l3dxSaveEditor")

def showMinusEditor():
    dpg.hide_item("editSaveWindow")
    dpg.hide_item("l3dxSaveEditor")
    dpg.show_item("minusSaveWindow")

if __name__ == "__main__":
    print("You are NOT supposed to run this directly!")
    print("Either run main.py or the compiled executable!")
    input()
    sys.exit()
