import sys
import os
import zipfile
from cx_Freeze import setup, Executable


if sys.platform.startswith('linux'):
    try:
        os.system("sudo apt install python3-pip -y")
        os.system("python3 -m pip3 install -r requirements.txt")
        os.system("sudo apt install python3-tk")
    except OSError as error:
        print(error)

elif sys.platform.startswith('win'):
    try:
        os.system("python -m pip install -r requirements.txt")
    except OSError as error:
        print(error)


build_exe_options = {"packages": ["os", "sys", "tkinter", "Tcl", "tk", "mysql", "dotenv"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Admin Estação",
    version = "0.1",
    description = "Painel da Estação Meteorológica",
    options = {"build_exe": build_exe_options},
    executables = [
        Executable("app/PainelEstacao.py", base=base, icon='app\\app_icon.ico')
    ]
)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file), 
                os.path.relpath(
                    os.path.join(root, file), 
                    os.path.join(path, '..')
                )
            )

os.system("copy .env build\exe.win-amd64-3.10")
os.system("copy app\\app_icon.ico build\exe.win-amd64-3.10")
os.system("ren build\exe.win-amd64-3.10 Painel-Estacao")

zipf = zipfile.ZipFile('Painel-Estação.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('build\\Painel-Estacao', zipf)
zipf.close()

os.system("ren build\Painel-Estacao exe.win-amd64-3.10")
os.system("build\exe.win-amd64-3.10\PainelEstacao.exe")