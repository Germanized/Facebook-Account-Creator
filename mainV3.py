import requests
from bs4 import BeautifulSoup
import random
import time
import threading
import os

failed_proxies = set()

def load_proxies():
    try:
        with open('proxies.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Proxy file not found.")
        return []

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

class FaceBook_RegIster():
    def __init__(self, use_proxies):
        self.session = requests.Session()
        self.use_proxies = use_proxies
        self.cookies = {
            "lsd": "",
            "jazoest": "",
            "ccp": "",
            "reg_instance": "",
            "submission_request": "",
            "reg_impression_id": "",
            "__s": "",
            "__hsi": ""
        }
        self.password = "".join(random.choice("1234567890qpwoeirutyalskdjfhgmznxbcv") for _ in range(10))
        self.email = "whisper" + "".join(random.choice("1234567890qpwoeirutyalskdjfhgmznxbcv") for _ in range(15))
        self.Name = "John"
        self.Name2 = "Lopez"
        self.done = False

    def run(self):
        if self.use_proxies:
            print("[+] Getting cookies ...")
            self.get_cookies()
        print('[+] Creating the account ...')
        self.register()

    def get_cookies(self):
        url = "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr"
        proxies = load_proxies() if self.use_proxies else []

        while True:
            proxy = random.choice(proxies) if self.use_proxies else None
            proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
            headers = {
                "User-Agent": get_random_user_agent()
            }

            try:
                r = self.session.get(url, headers=headers, proxies=proxy_dict if self.use_proxies else None, timeout=10)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    self.cookies['lsd'] = soup.select_one('input[name=lsd]')['value']
                    self.cookies['jazoest'] = soup.select_one('input[name=jazoest]')['value']
                    self.cookies['ccp'] = soup.select_one('input[name=ccp]')['value']
                    self.cookies['reg_instance'] = soup.select_one('input[name=reg_instance]')['value']
                    self.cookies['submission_request'] = soup.select_one('input[name=submission_request]')['value']
                    self.cookies['reg_impression_id'] = soup.select_one('input[name=reg_impression_id]')['value']
                    self.cookies['__s'] = soup.select_one('input[name=__s]')['value'] if soup.select_one('input[name=__s]') else ""
                    self.cookies['__hsi'] = soup.select_one('input[name=__hsi]')['value'] if soup.select_one('input[name=__hsi]') else ""
                    return
            except Exception as e:
                print(f"[-] Error: {e}")
                if proxy:
                    print(f"[-] Proxy {proxy} failed, skipping.")
                    failed_proxies.add(proxy)

    def save_to_text_file(self, username, email, password, status):
        with open('account_info.txt', 'a') as file:
            file.write(f'Username: {username}\n')
            file.write(f'Email: {email}\n')
            file.write(f'Password: {password}\n')
            file.write(f'Status: {status}\n')
            file.write('=' * 40 + '\n')

    def register(self):
        url = "https://mbasic.facebook.com/reg/submit/?cid=103"
        proxies = load_proxies() if self.use_proxies else []
        proxy = random.choice(proxies) if self.use_proxies else None
        proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
        headers = {
            "Host": "mbasic.facebook.com",
            "Cookie": f"datr={self.cookies['reg_instance']}",
            "User-Agent": get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://mbasic.facebook.com",
            "Dnt": "1",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
        }

        data = (
            f"lsd={self.cookies['lsd']}&jazoest={self.cookies['jazoest']}&ccp={self.cookies['ccp']}&reg_instance="
            f"{self.cookies['reg_instance']}&submission_request={self.cookies['submission_request']}&helper=&reg_impression_id="
            f"{self.cookies['reg_impression_id']}&ns=0&zero_header_af_client=&app_id=&logger_id=&field_names%5B%5D=firstname&field_names%5B%5D=reg_email__&field_names%5B%5D=sex&field_names%5B%5D=birthday_wrapper&field_names%5B%5D=reg_passwd__&firstname="
            f"{self.Name}&lastname={self.Name2}&reg_email__={self.email}%40yopmail.com&sex={random.randint(1,2)}&custom_gender=&did_use_age=false&birthday_month="
            f"{random.randint(1,12)}&birthday_day={random.randint(1,28)}&birthday_year={random.randint(1996,2005)}&age_step_input=&reg_passwd__={self.password}&submit=Sign+Up"
        )
        if self.cookies['__s']:
            data += f"&__s={self.cookies['__s']}"
        if self.cookies['__hsi']:
            data += f"&__hsi={self.cookies['__hsi']}"

        try:
            r = self.session.post(url, headers=headers, data=data, proxies=proxy_dict if self.use_proxies else None, timeout=10)
            
            if 'take you through a few steps to confirm your account on Facebook' in r.text:
                print('[+] Account created successfully!')
                print("[+] Email: " + self.email + "@yopmail.com")
                print("[+] Password: " + self.password)
                print("[+] Status: Confirm")
                print('=' * 40)
                self.save_to_text_file('Not Found', f'{self.email}@yopmail.com', self.password, 'Confirm')
            elif 'There was an error with your registration. Please try registering again.' in r.text:
                print('[X] Blocked from Facebook')
                print('=' * 40)
                self.save_to_text_file('Blocked', '', '', '')
            else:
                try:
                    user_id = r.cookies['c_user']
                    print('[+] Account created successfully!')
                    print('[+] Username: ' + user_id)
                    print("[+] Email: " + self.email + "@yopmail.com")
                    print("[+] Password: " + self.password)
                    print("[+] Status: Done Create Account")
                    print('=' * 40)
                    self.save_to_text_file(user_id, f'{self.email}@yopmail.com', self.password, 'Done Create Account')
                except KeyError:
                    print("[X] Use VPN or better proxy")
                    print('=' * 40)
                    self.save_to_text_file('', '', '', 'Use VPN')
        except Exception as e:
            print(f"[-] Error: {e}")

def display_menu():
    print('''#######################################################################################*......::::::::
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*..:::...::::::
%%%=:::::::::::#%+:::::::-+#%%%%%%%%%%%%%%%*:::=%%%%%%%%*+-::::-=+#%%%%%*=-::::-=*%%%%%*..::::....::::
%%%=........:::#%+::::::...:=%%%%%%%%%%%%%%:...:#%%%%%%-:.........:+%%%::.....:::::*%%%*:::::::::::...
%%%=..:#%%%%%%%%%+..:*%%%+:.:+%%%%%%%%%%%%=:::::=%%%%%*:::+%%%%#-:.:#%=...*%%%%#-..-#%%*:::::::::.....
%%%=:::#%%%%%%%%%+..:*%%%+:.:+%%%%%%%%%%%#:::::::*%%%%+:::#%%%%%#***#%-..:#%%%%%#***#%%*::::::::::....
%%%=:::++++++*#%%+.........:+%%%%%%%%%%%%=::-#-::+%%%%=:::#%%%%%%%%%%%-:::#%%%%%%%%%%%%*:..:::::::::..
%%%=::::.....-#%%+..:::::::::-#%%%%%%%%%*:.:=%=..:#%%%=...#%%%%%%%%%%%-:::#%%%%%%%%%%%%*::....::::::::
%%%=:::*######%%%+:::*%%%%*::::%%%%%%%%%+..:#%#...=%%%=...#%%%%%%%%%%%-:::#%%%%%%%%%%%%*........::::::
%%%=..:#%%%%%%%%%+:::*%%%%%=...#%%%%%%%#...........%%%+...#%%%%%#+++#%-:.:#%%%%%*++*#%%*:...........::
%%%=..:#%%%%%%%%%+:::*%%%%#:..:%%%%%%%%=..:::::::::-%%#:::=%%%%#-::-#%+::.+%%%%*:.:-#%%*:::...........
%%%=..:#%%%%%%%%%+..::::::...:*%%%%%%%#:::+%%%%%+:::*%%=:::::::::::#%%%-:::::::...:#%%%*::::::........
%%%=---#%%%%%%%%%+---------=*%%%%%%%%%=---#%%%%%#---+%%%#+=----==*%%%%%%#==-----=#%%%%%*:::::::::.....
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*..:::::::::...
#######################################################################################+......::::::::
::::::..........:::::::::::.............................::::...:::..........::::::::::..........::::::
::::......:+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
::........-#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
:........:-#%%%%%*====+#%%%%*====++#%%%%#========+#%%%%%#+#%%%+========+%%%%*=====#%%%%%*+===++#%%%%%%
........::-#%%%=:*%%%%#:-%%%+-#####=:+%%*:#%%%%%%%%%%%%%+.-%%%%%%%--%%%%%%=:*%%%%%+:+%%%+:#####+:+%%%%
.....:::::-#%%*:#%%%%%%%:+%%+=#%%%%%*-#%*:#%%%%%%%%%%%%#:+:#%%%%%%--%%%%%*:#%%%%%%%*-#%%+:#%%%%%*:#%%%
....::::::-#%%=-%%%%%%%%##%%+=#%%%%%*:#%*:#%%%%%%%%%%%%==%--%%%%%%--%%%%%=:%%%%%%%%#:*%%+:#%%%%%#:*%%%
..:::::::.-#%%=-%%%%%%%%%%%%+=#%%%%%*:#%*:#%%%%%%%%%%%#:*%#:#%%%%%--%%%%%=:%%%%%%%%#:*%%+:#%%%%%#:*%%%
::::::::..-#%%=-%%%%%%%%%%%%+=#%%%%%*-#%*:::::::-*%%%%--%%%-=%%%%%--%%%%%=:%%%%%%%%#:*%%+:#%%%%%*:#%%%
::::::....-#%%=-%%%%%%%%%%%%+-*###*-:*%%*:#%%%%%%%%%%#:#%%%#:*%%%%--%%%%%=:%%%%%%%%#:*%%+:*###*=:+%%%%
::::......-#%%=-%%%%%%%%%%%%+-*#*:+%%%%%*:#%%%%%%%%%%=:%%%%#=+%%%%--%%%%%=:%%%%%%%%#:*%%+:*#*--#%%%%%%
::::......-#%%=-%%%%%%%%+*%%+=#%%#-=%%%%*:#%%%%%%%%%*:======-:#%%%--%%%%%=:#%%%%%%%#:*%%+:#%%%--#%%%%%
::.......:-#%%*:#%%%%%%#:*%%+=#%%%#:-%%%*:#%%%%%%%%%+=#%%%%%#-+%%%--%%%%%#:*%%%%%%%*-#%%+:#%%%%=-#%%%%
........::-#%%%*-=+**+=:+%%%+=#%%%%%-=#%*:=+++++++##:+%%%%%%%+:#%%--%%%%%%*--+**++--*%%%+:#%%%%#=-#%%%
.......:::-#%%%%%######%%%%%%#%%%%%%%#%%%#########%%#%%%%%%%%%#%%%##%%%%%%%%######%%%%%%%#%%%%%%%##%%%
.....:::::-#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%''')

    print("\n" + "=" * 40)
    print("FB ACC creator 3.0 BETA By Germanized")
    print("=" * 40)
    print("1. Use proxy file")
    print("2. Run proxieless (likely to get blocked)")
    print("=" * 40)

    while True:
        choice = input("Choose an option: ")
        if choice in ['1', '2']:
            break
        else:
            print("Invalid choice, please choose again.")

    return choice

def main():
    choice = display_menu()
    use_proxies = True if choice == '1' else False

    num_accounts = input("How many accounts do you want to create? ")
    try:
        num_accounts = int(num_accounts)
    except ValueError:
        print("Invalid number, exiting.")
        return

    threads = []
    for _ in range(num_accounts):
        fb_register = FaceBook_RegIster(use_proxies)
        thread = threading.Thread(target=fb_register.run)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
