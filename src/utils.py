def OpenRealFileName(saveFileNumber, player):
    TempsaveFile = ""
    if saveFileNumber == "" or player == "" or saveFileNumber == "Save file 1":
        TempsaveFile = "saveData1.ini"
    elif saveFileNumber == "Save file 2" and player == "Peppino":
        TempsaveFile = "saveData2.ini"
    elif saveFileNumber == "Save file 3" and player == "Peppino":
        TempsaveFile = "saveData3.ini"
    elif saveFileNumber == "Save file 1" and player == "Noise":
        TempsaveFile = "saveData1N.ini"
    elif saveFileNumber == "Save file 2" and player == "Noise":
        TempsaveFile = "saveData2N.ini"
    elif saveFileNumber == "Save file 3" and player == "Noise":
        TempsaveFile = "saveData3N.ini"
    else:
        TempsaveFile = "saveData1.ini"  # fallback case if needed
    print(TempsaveFile)
