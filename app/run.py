import os
import sys


def run():
    if sys.platform.startswith('linux'):
        try:
            os.system("sudo apt install python3-pip -y")
            os.system("python3 -m pip3 install -r requirements.txt")
            os.system("sudo apt install python3-tk")
            os.system("python3 PainelEstacao.py")
        except OSError as error:
            print(error)
    
    elif sys.platform.startswith('win'):
        try:
            os.system("python -m pip install -r requirements.txt")
            os.system("python PainelEstacao.py")
        except OSError as error:
            print(error)


if __name__ == '__main__':
    run()
