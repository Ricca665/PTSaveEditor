import dearpygui.dearpygui as dpg
import configparser
import re
import pymsgbox
import sys

config = configparser.ConfigParser()

# Configuration logic

def OpenRealFileName(saveFileNumber, noise, savedatadir):
    """Opens the save file

    Args:
        saveFileNumber (String): The save file number (so save file 1, 2 and 3)
        noise (Boolean): If it's the noise's file
        savedatadir (String): The save file data location

    Returns:
        String: The full save file INI path
    """
    global saveFile
    TempsaveFile = ""

    #Decide the save file
    if saveFileNumber == "" or saveFileNumber == "Save file 1":
        TempsaveFile = "saveData1.ini"
    if saveFileNumber == "Save file 2":
        TempsaveFile = "saveData2.ini"
    if saveFileNumber == "Save file 3":
        TempsaveFile = "saveData3.ini"

    #True means that the noise checkbox is checked
    if noise:
        TempsaveFile = TempsaveFile.replace(".ini", "")
        TempsaveFile = TempsaveFile + "N.ini"

    saveFile = savedatadir+"/"+TempsaveFile

    try:
        with open(saveFile, "r") as f: # Tries to open and read the contents of the file
            saveFileContents = f.read() 
        dpg.set_value("file_contents", saveFileContents)
        dpg.show_item("editSaveWindow")
    
    except Exception as e: # In case it can't
        pymsgbox.alert(f"The save file does not exist, or a unknown error has occurred!\n Stack trace: \n{e}", "Error! Please contact riccar10210 on discord!") # Show the error message

    return saveFile

def getInternalNameFromExternal(extname):
    """Gets the referenced internal name from friendly ones

    Args:
        extname (string): The friendly name of the level (e.g. John gutter)

    Returns:
        string: The referenced internal name (e.g. entrance)
    """
    level = extname.lower()
    # Normal levels
    # Floor 1
    if level == "john gutter":
        return "entrance"
    elif level == "pizzascape":
        return "medieval"
    elif level == "ancient cheese":
        return "ruin"
    elif level == "bloodsauce dungeon":
        return "dungeon"
    # Floor 2
    elif level == "oregano desert":
        return "badland"
    elif level == "wasteyard":
        return "graveyard"
    elif level == "fun farm":
        return "farm"
    elif level == "fastfood saloon":
        return "saloon"
    # Floor 3
    elif level == "crust cove":
        return "plage"
    elif level == "gnome forest":
        return "forest"
    elif level == "deep-dish 9":
        return "space"
    elif level == "golf":
        return "minigolf"
    # Floor 4
    elif level == "the pig city":
        return "street"
    elif level == "peppibot factory":
        return "industrial"
    elif level == "oh shit!":
        return "sewer"
    elif level == "rrf" or level == "refrigerator-refrigerador-freezerator": # check for both conditions
        return "freezer"
    # Floor 5
    elif level == "pizzascare":
        return "chateau"
    elif level == "dmas":
        return "kidsparty"
    elif level == "war":
        return "war"
    elif level == "ctop":
        return "exit"
    
    # Bosses
    elif level == "pepperman":
        return "b_pepperman"
    elif level == "vigilante":
        return "b_vigilante"
    elif level == "noise":
        return "b_noise"
    elif level == "fake peppino":
        return "b_fakepep"
    
    # Default return value
    return "invalid"

def CleanSaveFileGarbage():
    """Cleans the save file garbage"""

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

def INISetup():
    """Sets up the INI Configuration to be read and written to"""
    CleanSaveFileGarbage()
    config.read(saveFile) # Reads the save file
    return

def INICloseAndWrite():
    """Closes and saves the new INI Configuration"""
    with open(saveFile, "w") as newSaveFile: # Opens the file
        config.write(newSaveFile) # Writes it back
    showDoneWindow() # Shows the done window
    return

# Flag setter logic
def ReviveSnotty():
    INISetup()

    if "Game" not in config:
        config["Game"] = {}

    config["Game"]["snotty"] = '"0.000000"'  # Sets the snotty flag to 0, meaning snotty hasn't been killed

    INICloseAndWrite()

def SetCTOPLappingMinusLap():
    INISetup()

    if "Unlocks" not in config:
        config["Unlocks"] = {}
    
    config["Unlocks"]["minus_tctop"] = f'"1"'

    INICloseAndWrite()

# Ranks setter logic
def l3dxSetRanks(level, rank, keys):
    INISetup()

    level = getInternalNameFromExternal(level)

    if "Lapped3" not in config:
        config["Lapped3"] = {}
    
    if "3Rank" not in config:
        config["3Rank"] = {}
    
    if "LapKey" not in config:
        config["LapKey"] = {}

    level = str(level)+"6" # L3DX saves the data for each level as level+6 and then the value
                           # By doing this we are doing it just once
                           # so if the level was "entrance" (AKA John gutter) it would be entrance6

    config["Lapped3"][level] = f'"2.000000"' # Tell that we did indeed lap it

    config["3Rank"][level] = f'"{rank}"' # Rank

     # The keys for each level are saved separately
    
    if keys:
        config["LapKey"][level] = f'"1.000000"'
    else:
        config["LapKey"][level] = f'"0.000000"'

    INICloseAndWrite()
    

def SetRanks(level, rank, gerome, secrets, score):
    INISetup()
    level = getInternalNameFromExternal(level)

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

    INICloseAndWrite()

def SetLapMinusRanks(level, rank, islapminus, lap):
    INISetup()
    level = getInternalNameFromExternal(level)

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
    # 1            2        Lap 2 M Rank (below this is just a normal s rank)
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

    decidedrank = 0 # When rank is 0 it means that no rank is set

    # For this follow the table above
    if islapminus:
        if lap == "lap 5":
            if rank == "p":
                decidedrank = 7
            else:
                decidedrank = 6
        elif lap == "lap 4":
            if rank == "p":
                decidedrank = 5
            else:
                decidedrank = 4
        elif lap == "lap 3":
            if rank == "p":
                decidedrank = 3
            else:
                decidedrank = 2
        elif lap == "lap 2":
            if rank == "p":
                decidedrank = 1
            else:
                deciderank = 0
        else:
            rank = 0
        config["LapMinusNegative"][str(level)] = f'"{decidedrank}"' # Modify the rank
    else:
        if lap == "lap 5":
            if rank == "p":
                decidedrank = 6
            else:
                decidedrank = 5
        elif lap == "lap 4":
            if rank == "p":
                decidedrank = 4
            else:
                decidedrank = 3
        elif lap == "lap 3":
            if rank == "p":
                decidedrank = 2
            else:
                decidedrank = 1
        else:
            decidedrank = 0
        config["LapMinusPositive"][str(level)] = f'"{decidedrank}"' # Modify the rank
        
    INICloseAndWrite() # Close the INI and save

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

def OpenMainScreen():
    save = dpg.get_value("file_contents")
    save = str(save)  # Convert to string
    
    with open(saveFile, "r+") as f: # Writes it
        f.write(save)
        f.truncate()
    
    dpg.hide_item("rawEditor") # Hides the editor
    dpg.show_item("editSaveWindow") # Shows the main menu

#TODO Maybe rewrite this logic?
# I noticed that we should only need a show_item
def showL3DXEditor():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("l3dxSaveEditor")

def showMinusEditor():
    dpg.hide_item("editSaveWindow")
    dpg.hide_item("l3dxSaveEditor")
    dpg.show_item("minusSaveWindow")

def showDoneWindow():
    #Adapted from: https://github.com/hoffstadt/DearPyGui/discussions/1002
    # guarantee these commands happen in the same frame
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label="Done!", modal=True, no_close=True, no_title_bar=True, no_resize=True) as modal_id:
            dpg.add_text("Done!")
            dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=lambda:dpg.delete_item(modal_id))
            
    # guarantee these commands happen in another frame
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])
    
if __name__ == "__main__":
    print("You are NOT supposed to run this directly!")
    print("Either run main.py or the compiled executable!")
    input()
    sys.exit()
