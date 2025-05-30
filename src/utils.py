import dearpygui.dearpygui as dpg
import configparser
config = configparser.ConfigParser()
def OpenRealFileName(saveFileNumber, player, savedatadir):
    global saveFile
    TempsaveFile = ""
    print(saveFileNumber)
    print(player)
    if saveFileNumber == "" or player == "" or saveFileNumber == "Save file 1":
        TempsaveFile = "saveData1.ini"
    if saveFileNumber == "Save file 2" and (player == "Peppino" or player == ""):
        TempsaveFile = "saveData2.ini"
    if saveFileNumber == "Save file 3" and (player == "Peppino" or player == ""):
        TempsaveFile = "saveData3.ini"
    if saveFileNumber == "Save file 1" and player == "Noise":
        TempsaveFile = "saveData1N.ini"
    if saveFileNumber == "Save file 2" and player == "Noise":
        TempsaveFile = "saveData2N.ini"
    if saveFileNumber == "Save file 3" and player == "Noise":
        TempsaveFile = "saveData3N.ini"
    else:
        TempsaveFile = "saveData1.ini"  # fallback case if needed
    saveFile = savedatadir+"/"+TempsaveFile
    print(saveFile)
    with open(saveFile, "r") as f:
        saveFileContents = f.read()
    dpg.set_value("file_contents", saveFileContents)
    dpg.show_item("editSaveWindow")
    return saveFile

def ReviveSnotty():
    pass
def GetPRank():
    with open(saveFile, "rb") as f: # opens the file
        data = f.read()
    
    #This instruction is REQUIRED since pizza tower, for some reason, adds ending bytes to the end, this fixes the issue
    saveFileCleaned = data.replace(b'\00', b'')  # Removes those bytes

    with open(saveFile, "wb") as f: # Write the clean save file
        f.write(saveFileCleaned)

    config.read(saveFile) # Rereads the save file with configparser, this let's us modify specific sections OF the file
    
    level_list = ["entrance", "medieval", "ruin", "dungeon", "b_pepperman",
                  "badland", "graveyard", "farm", "saloon", "b_noise", "b_vigilante",
                  "b_fakepep", "pizzarush", "trickytreat", "entrway", "exit", "chateau",
                  "kidsparty", "freezer", "street", "industrial", "space", "plage",
                  "forest", "minigolf", "sewer", "war"]
    
    with open(saveFile, "r") as f:
        saveFileContents = f.readlines() # Reads every line of the file
    
    for level in level_list:
        config["Ranks"][level] = '"p"'  # Compares each file in the Ranks section of the file and changes it to be a p rank
    
    with open(saveFile, "w") as configfile: # Rewrites the save file back
        config.write(configfile)

def OpenRAWEditor():
    dpg.hide_item("editSaveWindow")
    dpg.show_item("rawEditor")

def OpenMainScreen():
    save = dpg.get_value("file_contents")
    save = str(save)  # Convert to string just in case
    print(save)
    with open(saveFile, "r+") as f:
        f.write(save)
        f.truncate()
    
    dpg.hide_item("rawEditor")
    dpg.show_item("editSaveWindow")
