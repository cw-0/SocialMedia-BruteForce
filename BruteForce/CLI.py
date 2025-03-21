import sys
import os
import typing
import pyfiglet
from colorama import just_fix_windows_console, Fore, Back, Style
import time

from .instagram_attack import Instagram

instagram = Instagram()

class Menu():
        menu_options = {
            "1": "Instagram",
            "2": "Epic Games",
            "3": "Twitch",
            "4": "Discord",
            "5": "Chat GPT",
            "6": "Steam",
            "7": "Twitter" 
        }
        
        def __init__(self):
            self.alert = None
            self.invalid_selection = (Fore.RED + "Invalid Selection" + Style.RESET_ALL).center(50)
            self.unimplemented_alert = (Fore.RED + "Not Yet Implemented" + Style.RESET_ALL).center(50)

        
        def show_menu(self):
            for k, v in self.menu_options.items():
                print(f"{k}. {v}")
            print("\nq. Quit\n")



        def run(self):
            while True:
                self.clear_screen()
                print(pyfiglet.figlet_format("Brute Forcer", font="big"))
                self.show_alert()
                self.show_menu()
                
                choice = input(">> ").strip()
                if choice == "1":
                    self.reset_alert()
                    print()
                    try:
                        instagram.attack()
                    except Exception:
                        pass

                elif choice == "2":
                    self.alert = self.unimplemented_alert
                
                elif choice == "3":
                    self.alert = self.unimplemented_alert

                elif choice == "4":
                    self.alert = self.unimplemented_alert
                
                elif choice == "5":
                    self.alert = self.unimplemented_alert

                elif choice == "6":
                    self.alert = self.unimplemented_alert

                elif choice == "7":
                    self.alert = self.unimplemented_alert

                elif choice.lower() == "q":
                    sys.exit()

                else:
                    self.alert = self.invalid_selection
        
        @staticmethod
        def clear_screen():
            os.system("cls" if os.name == "nt" else "clear")


        def reset_alert(self):
            self.alert = None

        def show_alert(self):
            print(self.alert + "\n\n" if self.alert and self.alert is not None else "\n\n")
        
            



if __name__ == "__main__":
     menu = Menu()
     menu.run()
