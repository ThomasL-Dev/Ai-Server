import os
import sys

from rich import print
from rich.console import Console
from rich.table import Table

from binaries.Logger import Logger
log = Logger()
# ========================================== FIN DES IMPORTS ========================================================= #


class ConsoleDebug:


    @staticmethod
    def clear_console():
        if sys.platform == "win32":
            os.system('cls')
        elif sys.platform == "linux":
            os.system('clear')


    @staticmethod
    def set_title(title=''):
        if sys.platform == 'win32':
            os.system('title ' + title)
        else:
            sys.stdout.write('\33]0;' + title + '\a')
            sys.stdout.flush()


    @staticmethod
    def set_console_size():
        # resize console
        if sys.platform == 'linux':
            _CONSOLE_WIDTH = 95  # 83
            _CONSOLE_HEIGHT = 25
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=_CONSOLE_HEIGHT, cols=_CONSOLE_WIDTH + 10))


    @staticmethod
    def print(text: str, color="blue"):
        print("[bold " + color + "]" + text + "[/bold " + color + "]")
        log.info(text)


    @staticmethod
    def link(text: str, link: str, color="magenta", protocol="https", end_link="/"):
        if not link.startswith("http://") or not link.startswith("https://"):
            link = protocol + "://" + link + end_link
        print("[bold " + color + "][link=" + link + "]" + text + "[/link][/bold " + color + "]")
        log.info(text)


    @staticmethod
    def info(text: str, color="yellow"):
        print("[bold " + color + "][INFO] " + text + "[/bold " + color + "]")
        log.info(text)


    @staticmethod
    def kernel(text: str):
        color = "cyan"
        print("[bold " + color + "][KERNEL] " + text + "[/bold " + color + "]")
        log.log(text)


    @staticmethod
    def exact(text: str):
        color = "green"
        print("[bold " + color + "][KERNEL] " + text + "[/bold " + color + "]")
        log.info(text)


    @staticmethod
    def error(text: str):
        color = "red"
        print("[bold " + color + "][ERROR] " + text + "[/bold " + color + "]")
        log.error(text)


    @staticmethod
    class table:
        def __init__(self, title: str, color="bold cyan"):
            self.console = Console()
            self.table = Table(title=title, header_style=color)

        def add_column(self, title: str, text_pos="center", color='magenta'):
            self.table.add_column(title, justify=text_pos, style=color)

        def add_row(self, *args):
            self.table.add_row(*args)

        def show(self):
            self.console.print(self.table)
