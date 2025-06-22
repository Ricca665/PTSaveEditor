import os
import subprocess
import zipfile
import shutil
from builder_utils import *

"""Compiler options"""
compiler = "pyinstaller" # Compiler
compiler_flags = '--onefile --windowed src/main.py --name="PTSaveFileEditor.exe" --clean --noupx ' \
                    '--version-file=version.txt' # Compiler flags, version.txt to bypass retarded AVs,  mf i have AVs now 🌹🌹
libs = ["dearpygui", compiler, "pymsgbox"] # Required libraries 

version_number = "4" # The version number of the program
def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__))) # Enters the current directory where the builder is found, this fixes the "Script file 'src/main.py' does not exist." error when compiling
    try:
        shutil.rmtree("dist")
        shutil.rmtree("output")
    except:
        pass

    print("Step 1/3: installing required libs")
    install_libs(libs)
    print("Finished installing libs")

    print("Step 2/3: Compiling program")
    print(f"Compiler of choice: {compiler}") # Shows the compiler that is going to be used
    print(f"Compiler flags: {compiler_flags}") # Shows the compiler flags
    print(f"Building with the following command:\n{compiler} {compiler_flags}")
    compile(compiler, compiler_flags)

    print("Step 3/3: Zipping program")
    zipfilepath = f"../output/PTSaveFileEditorV{version_number}.zip"
    packageExec(zipfilepath)

    print("Done! Check for any errors")

if __name__ == "__main__":
    main()
