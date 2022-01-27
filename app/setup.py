import sys
import os

if sys.platform.startswith('linux'):
    try:
        os.system("sudo apt install python3-pip -y")
        os.system("python3 -m pip3 install -r requirements.txt")
        os.system("sudo apt install python3-tk")
        os.system("sudo apt install patchelf -y")
    except OSError as error:
        print(error)

elif sys.platform.startswith('win'):
    try:
        os.system("python -m psys.platform.startswith('win'):ip install -r requirements.txt")
    except OSError as error:
        print(error)

else:
    print("Erro!")

import zipfile
from cx_Freeze import setup, Executable


build_exe_options = {"packages": ["os", "sys", "tkinter", "Tcl", "tk", "mysql", "dotenv"]}

base = None
icon = 'app_icon.ico'
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Admin Estação",
    version = "0.0.1-alpha",
    description = "Painel da Estação Meteorológica",
    options = {"build_exe": build_exe_options},
    executables = [
        Executable("PainelEstacao.py", base=base, icon='app_icon.ico')
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

p_v = str(sys.version_info[0])+'.'+str(sys.version_info[1])

if sys.platform.startswith('win'):
    os.system(f"copy .env build\exe.win-amd64-{p_v}")
    os.system(f"attrib +h build\exe.win-amd64-{p_v}\.env && attrib +h build\exe.win-amd64-{p_v}\\app_icon.ico && attrib +h build\exe.win-amd64-{p_v}\python3.dll && attrib +h build\exe.win-amd64-{p_v}\python310.dll")
    os.system(f"ren build\exe.win-amd64-{p_v} Painel-Estacao")

    zipf = zipfile.ZipFile('Painel-Estação.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('build\\Painel-Estacao', zipf)
    zipf.close()

    os.system(f"ren build\Painel-Estacao exe.win-amd64-{p_v}")
    os.system(f"cd build\exe.win-amd64-{p_v} && PainelEstacao.exe")

elif sys.platform.startswith('linux'):
    os.system(f"cp .env build/exe.linux-x86_64-{p_v}")
