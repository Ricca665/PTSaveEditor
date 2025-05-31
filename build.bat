echo "Step 1/2: Installing required libs (dearpygui, pyinstaller)"
pip install dearpygui pyinstaller

echo "Step 2/2: Compiling code into executable..."
pyinstaller --onefile --windowed src/main.py --name="PTSaveFileEditor.exe" --clean

echo "Done! Check for any errors during compilation and/or libs installing"