from colorama import Fore, init
from Consolly import consoler
import easygui
import random
import requests, os, sys
import json
from time import sleep, strftime, time, gmtime
init()
console = consoler()
unix = str(strftime('[%d-%m-%Y %H-%M-%S]'))
steam_key = '' # Steam key is a steam api key

dater = {
    "discord": {
        "webhook": "false",
        "url": "",
        "send_invalids": "false",
        "send_valids": "true",
        "valid_mention_everyone": "true"
    }
}

class Counter:
    valid = 0
    unvalid = 0
    proxies = 0
    names = 0
    retries = 0
    cpm = 0

class Program:
    def __init__(self):
        self.api_url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1'
        self.proxies_api = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all'
        self.og_names = 'https://raw.githubusercontent.com/beeteo/ognames/main/og.txt'
        self.names = []
        self.proxies = []
        self.timer = 0
        self.checked = 0
        self.checkfiles()
        self.main()
    
    def checkfiles(self):
        if not os.path.exists('Results'):
            os.mkdir('Results')
        
        if not os.path.exists('discord.json'):
            with open('discord.json', 'w') as f:
                json.dump(dater, f, indent=4)

    def now_time(self):
        return strftime("%H:%M:%S", gmtime(time() - self.timer))

    def updatetitle(self):
        self.timer = time()
        while True:
            return console.set_title(f'Steam-Vanity URL | Valid URLS: {Counter.valid} | Unvalid URLS: {Counter.unvalid} | Remaining: {Counter.names}/{Counter.names - self.checked} - beete#2766')

    def check(self, name):
        with open('discord.json') as f:
            discord = json.load(f)
        
        path = f'Results/{unix}'

        a = {
            'key': steam_key
        }

        data = requests.get(
            url = self.api_url + '?vanityurl={}'.format(name),
            params = a,
            proxies = random.choice(self.proxies)
        )

        if '{"success":42,"message":"No match"}' in data.text:
            print(f'{Fore.LIGHTGREEN_EX}{name} {Fore.WHITE}| {Fore.CYAN}https://steamcommunity.com/id/{name}{Fore.WHITE} | Status: {Fore.LIGHTGREEN_EX}Valid!')
            Counter.valid += 1
            self.checked += 1

            if discord['discord']['valid_mention_everyone'] == 'true':
                mention = '@everyone'
            else:
                mention = ''

            if discord['discord']['webhook'] == 'true':
                wb = {'content': f'{name} | https://steamcommunity.com/id/{name} | - Valid - {mention}'}

                requests.post(discord['discord']['url'], data=wb)
            
            if not os.path.exists(path):
                os.mkdir(path)

            open(f'Results/{unix}/Valid URLS.txt', 'a').write(f'{name} | https://steamcommunity.com/id/{name} | Valid\n')
        else:
            if not os.path.exists(path):
                os.mkdir(path)

            Counter.unvalid += 1
            self.checked += 1
            try:
                converter = data.json()
                print(f'{Fore.RED}{name} {Fore.WHITE}| {Fore.CYAN}https://steamcommunity.com/id/{name}{Fore.WHITE} | Status: {Fore.LIGHTRED_EX}Invalid{Fore.WHITE} | {Fore.CYAN}{converter["response"]["steamid"]}')
                open(f'Results/{unix}/Invalid URLS.txt', 'a').write(f'{name} | https://steamcommunity.com/id/{name} | Invalid\n')
            except:
                print(f'{Fore.RED}{name} {Fore.WHITE}| {Fore.CYAN}https://steamcommunity.com/id/{name}{Fore.WHITE} | Status: {Fore.LIGHTRED_EX}Invalid{Fore.WHITE} | {Fore.LIGHTBLACK_EX}None')
                open(f'Results/{unix}/Invalid URLS.txt', 'a').write(f'{name} | https://steamcommunity.com/id/{name} | Invalid\n')

    def main(self):
        console.set_title('Owo-nity Steam URL -- Menu uwu')

        names = input('Do you want to use og names extracted from a page?\nIf so, enter "Y" otherwise and if you already have a txt file with your og enter "N"\n> ')
        
        if names == 'y':
            og = requests.get(self.og_names).text.split('\n')   
            for i in og:
                self.names.append(i)
                Counter.names += 1
        else:
            names_path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'OG - Selector', multiple= False)
            with open(names_path, 'r', encoding="utf-8", errors='ignore') as f:
                for i in f:
                    self.names.append(i.split('\n')[0])
                    Counter.names += 1
        
        proxies_ = input('You want to use proxies from an api\nIf so, enter "Y" otherwise if you have proxies in a txt enter "N"\n> ')

        if proxies_ == 'y':
            loader = requests.get(self.proxies_api).text.splitlines()
            for l in loader:
                ip = l.split(":")[0]
                port = l.split(":")[1]
                self.proxies.append({'http': 'socks4' +'://'+ip+':'+port.rstrip("\n")})
        else:
            proxies_path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'OG - Proxies Selector', multiple= False)
            proxy_type = input('Enter your proxies type\n[1] HTTPS\n[2] SOCKS4\n[3] SOCKS5\n> ')
            
            if proxy_type == '1':
                proxytype = 'https'
            elif proxy_type == '2':
                proxytype = 'socks4'
            elif proxy_type == '3':
                proxytype = 'socks5'

            with open(proxies_path, 'r', encoding="utf-8", errors='ignore') as f:
                for l in f:
                    ip = l.split(":")[0]
                    port = l.split(":")[1]
                    self.proxies.append({'http': proxytype+'://'+ip+':'+port.rstrip("\n")})
        
        console.clear()
        for i in self.names:
            self.updatetitle()
            self.check(name=i)
        input('[+] Done, all checked!\n\n[+] Press enter to continue.')
        self.main()

if __name__ == '__main__':
    Program()
