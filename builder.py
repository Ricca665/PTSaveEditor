import os
import subprocess

"""Compiler options"""
libs = ["dearpygui", "pyinstaller", "pymsgbox"] # Required libraries 
compiler = "pyinstaller" # Compiler
compiler_flags = ' --onefile --windowed src/main.py --name="PTSaveFileEditor.exe" --clean' # Compiler flags


print("Step 1/2: installing required libs")
for lib in libs: # For each library
    print(f"Installing {lib}...") # Display the current library to install
    subprocess.run(["pip", "install", lib]) # Installs the library

print("Finished installing libs")

print("Step 2/2: Compiling program")
print(f"Compiler of choice: {compiler}") # Shows the compiler that is going to be used
print(f"Compiler flags: {compiler_flags}") # Shows the compiler flags
print(f"Building with the following command:\n{compiler+compiler_flags}")
os.system(f"{compiler+compiler_flags}") # Runs the compiler with flags

print("Done! Check for any errors")