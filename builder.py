import os
import subprocess
import zipfile
import shutil

"""Compiler options"""
compiler = "pyinstaller" # Compiler
compiler_flags = '--onefile --windowed src/main.py --name="PTSaveFileEditor.exe" --clean --noupx ' \
                    '--version-file=version.txt' # Compiler flags, version.txt to bypass retarded AVs,  mf i have AVs now 🌹🌹
libs = ["dearpygui", compiler, "pymsgbox"] # Required libraries 


version_number = "3" # The version number of the program

os.chdir(os.path.dirname(os.path.realpath(__file__))) # Enters the current directory where the builder is found, this fixes the "Script file 'src/main.py' does not exist." error when compiling
try:
    shutil.rmtree("dist")
    shutil.rmtree("output")
except:
    pass

print("Step 1/3: installing required libs")
for lib in libs: # For each library
    print(f"Installing {lib}...") # Display the current library to install
    subprocess.run(["pip", "install", lib]) # Installs the library

print("Finished installing libs")

print("Step 2/3: Compiling program")
print(f"Compiler of choice: {compiler}") # Shows the compiler that is going to be used
print(f"Compiler flags: {compiler_flags}") # Shows the compiler flags
print(f"Building with the following command:\n{compiler} {compiler_flags}")
os.system(f"{compiler} {compiler_flags}") # Runs the compiler with flags

print("Step 3/3: Zipping program")
try:
    os.makedirs("output")
except:
    pass
shutil.copyfile("dist/PTSaveFileEditor.exe", "output/PTSaveFileEditor.exe")
os.chdir("output")
zip = zipfile.ZipFile(f"PTSaveFileEditorV{version_number}.zip", "w", zipfile.ZIP_DEFLATED)
zip.write("PTSaveFileEditor.exe")

print("Done! Check for any errors")