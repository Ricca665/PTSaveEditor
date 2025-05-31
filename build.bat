echo off
cls
echo "Step 1/2: Installing required libs (dearpygui, py2exe)"
pip install dearpygui nuitka

echo "Step 2/2: Compiling code into executable..."
nuitka --standalone --onefile --output-filename=PTSaveEditor.exe src/main.py

echo "Done! Check for any errors during compilation and/or libs installing"
pause