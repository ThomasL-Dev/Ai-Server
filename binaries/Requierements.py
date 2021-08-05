import os
import sys
import time
# ========================================== FIN DES IMPORTS ========================================================= #



list_to_install = {
        "pip": [
            "rich",
            "requests",
            "tornado",
            "discord",
            "getmac",
            "pylgtv",
            "pywebostv",
            "pythoncom",
            "pywin32",
            "win32gui",
            "win32com",
            "Pillow",
            "pyftpdlib",
            "opencv-python",
            "numpy",
            "Pillow",
            "pyttsx3",
        ],

        "apt": [
            "python3-alsaaudio",
            "sox",
            "libsox-fmt-all",
            "libttspico-utils",
            "sox",
            "libsox-fmt-all",
            "libttspico-utils",
            "espeak",
        ],

    }




def __install_with_apt(pkg_name: str):
    try:
        import apt
        cache = apt.cache.Cache()
        cache.update()
        cache.open()

        pkg = cache[pkg_name]
        if pkg.is_installed:
            pass
        else:
            pkg.mark_install()

            try:
                cache.commit()
            except:
                pass
        time.sleep(0.5)
    except apt.cache.LockFailedException:
        print("Need to launch this program with sudo")
        sys.exit(0)

def __install_with_pip(pkg_name: str):
    if "win32" in sys.platform:
        import subprocess
        try:
            __import__(pkg_name, globals(), locals(), ['*'])
            print(pkg_name, "already installed")
        except:
            try:
                print("Downloading", pkg_name)
                subprocess.call(['pip3', 'install', str(pkg_name)], creationflags=0x08000000)
            except:
                pass
        
    else:
        try:
            from pip import main as pipmain
        except:
            from pip._internal.main import main as pipmain

        try:
            __import__(pkg_name, globals(), locals(), ['*'])
            print(pkg_name, "already installed")
        except:
            try:
                print("Downloading", pkg_name)
                pipmain(['install', pkg_name])
            except:
                pass
        
    time.sleep(0.5)


def __clear_console():
    if "win32" in sys.platform:
        os.system('cls')
    else:
        os.system('clear')


def install_requierement():
    if not os.path.exists(os.path.join(".cfg", "pass_install.txt")):
        # install pip dependancies
        for pkg in list_to_install['pip']:
            if pkg != "":
                __install_with_pip(pkg)
                __clear_console()


        if sys.platform == "linux":
            # install apt dependancies
            for pkg in list_to_install['apt']:
                if pkg != "":
                    __install_with_apt(pkg)
                    __clear_console()






