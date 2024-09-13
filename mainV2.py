import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent

proxies = [
    '103.140.205.133:1080',
    # Add more if u want idgaf
]

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

class FaceBook_RegIster():
    def __init__(self):
        self.session = requests.Session()
        self.done = False
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
        self.admin()

    def admin(self):
        print("[+] Getting cookies ...")
        time.sleep(random.uniform(2, 5))
        self.get_cookies()
        print('[+] Creating the account ...')
        time.sleep(random.uniform(2, 5))
        self.register()

    def get_cookies(self):
        url = "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr"
        
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}
        headers = {
            "User-Agent": get_random_user_agent()
        }
        
        r = self.session.get(url, headers=headers, proxies=proxy_dict)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        self.cookies['lsd'] = soup.select_one('input[name=lsd]')['value']
        self.cookies['jazoest'] = soup.select_one('input[name=jazoest]')['value']
        self.cookies['ccp'] = soup.select_one('input[name=ccp]')['value']
        self.cookies['reg_instance'] = soup.select_one('input[name=reg_instance]')['value']
        self.cookies['submission_request'] = soup.select_one('input[name=submission_request]')['value']
        self.cookies['reg_impression_id'] = soup.select_one('input[name=reg_impression_id]')['value']

        try:
            self.cookies['__s'] = soup.select_one('input[name=__s]')['value']
            self.cookies['__hsi'] = soup.select_one('input[name=__hsi]')['value']
        except TypeError:
            print("Couldn't find __s or __hsi values")

    def save_to_text_file(self, username, email, password, status):
        with open('account_info.txt', 'a') as file:
            file.write(f'Username: {username}\n')
            file.write(f'Email: {email}\n')
            file.write(f'Password: {password}\n')
            file.write(f'Status: {status}\n')
            file.write('=' * 40 + '\n')

    def register(self):
        url = "https://mbasic.facebook.com/reg/submit/?cid=103"
        
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}
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

        r = self.session.post(url, headers=headers, data=data, proxies=proxy_dict)
        
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

while True:
    FaceBook_RegIster()
