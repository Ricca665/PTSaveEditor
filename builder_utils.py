import subprocess
import zipfile
import os
import sys
import shlex

def install_libs(libs):
    for lib in libs: # For each library
        print(f"Installing {lib}...") # Display the current library to install
        subprocess.run([sys.executable, "-m", "pip", "install", lib]) # Installs the library
    
def compile(compiler, flags):
    flags_splitted = shlex.split(flags)
    subprocess.run([compiler, *flags_splitted])


def packageExec(zipfilepath):
    try:
        os.makedirs("output")
    except:
        pass

    os.chdir("dist")
    zip = zipfile.ZipFile(zipfilepath, "w", zipfile.ZIP_DEFLATED) # Zips the file
    zip.write("PTSaveFileEditor.exe")
    zip.close()

if __name__ == "__main__": # IN case the builder doesn't get invoked
    import builder
    print("Builder.py not invoked! Installing neccesary libs...")
    install_libs(builder.libs)
    print("Done!")