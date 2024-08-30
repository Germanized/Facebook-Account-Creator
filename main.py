import requests
from bs4 import BeautifulSoup
import random

class FaceBook_RegIster():
    def __init__(self):
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
        print("[+] get cookies ..")
        self.get_cookies()
        print('[+] Create The Account ..')
        self.register()

    def get_cookies(self):
        url = "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr"
        r = requests.get(url)
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
        headers = {
            "Host": "mbasic.facebook.com",
            "Cookie": f"datr={self.cookies['reg_instance']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://mbasic.facebook.com/reg/?cid=103&refsrc=deprecated&_rdr",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "547",
            "Origin": "https://mbasic.facebook.com",
            "Dnt": "1",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Te": "trailers"
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

        r = requests.post(url, headers=headers, data=data)
        if 'take you through a few steps to confirm your account on Facebook' in r.text:
            print('[+] Done Create Account !')
            print('[+] Username : Not Found ( Login Use Email )')
            print("[+] Email :" + self.email + "@yopmail.com")
            print("[+] Password : " + self.password)
            print("[+] Status : Confirm")
            print('=' * 40)
            self.save_to_text_file('Not Found', f'{self.email}@yopmail.com', self.password, 'Confirm')
        elif 'There was an error with your registration. Please try registering again.' in r.text:
            print('[X] Blocked From Facebook')
            print('=' * 40)
            self.save_to_text_file('Blocked', '', '', '')
        else:
            try:
                user_id = r.cookies['c_user']
                print('[+] Done Create Account !')
                print('[+] Username : '+user_id)
                print("[+] Email :" + self.email + "@yopmail.com")
                print("[+] Password : " + self.password)
                print("[+] Status : Done Create Account")
                print('=' * 40)
                self.save_to_text_file(user_id, f'{self.email}@yopmail.com', self.password, 'Done Create Account')
            except:
                print("[X] Use Vpn")
                print('=' * 40)
                self.save_to_text_file('', '', '', 'Use VPN')

while True:
    FaceBook_RegIster()
