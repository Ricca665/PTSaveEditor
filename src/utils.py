def OpenRealFileName(saveFileNumber, player, savedatadir):
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
    print(TempsaveFile)
    with open(savedatadir+"/"+TempsaveFile, "w") as f:
        saveFileContents = f.read()
    return saveFileContents
