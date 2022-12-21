import colorama
from colorama import Fore
colorama.init(strip=False)
def printWarning(text):
    print(Fore.YELLOW + text + Fore.RESET)
def printError(text):
    print(Fore.RED + text + Fore.RESET)
def printRed(text):
    print(Fore.RED + text + Fore.RESET)
def printYellow(text):
    print(Fore.YELLOW + text + Fore.RESET)
def printBlue(text):
    print(Fore.BLUE + text + Fore.RESET)
def printCyan(text):
    print(Fore.CYAN + text + Fore.RESET)
def printGreen(text):
    print(Fore.GREEN + text + Fore.RESET)
def printMagenta(text):
    print(Fore.MAGENTA + text + Fore.RESET)