import requests
import random
import string
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

url = "https://create.kahoot.it/rest/users"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "baggage": "",
    "Connection": "keep-alive",
    "Content-Length": "216",
    "Content-Type": "application/json",
    "Cookie": "",
    "Host": "create.kahoot.it",
    "Origin": "https://create.kahoot.it",
    "Referer": "https://create.kahoot.it/auth/register/signup-options?deviceId=2aMwhb0q-1IX0wG1tEIxE1&sessionId=1725907674171",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "sentry-trace": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "X-Kahoot-Tracking": "platform/Web"
}

def create_account(thread_id):
    random_letters = ''.join(random.choices(string.ascii_lowercase, k=7))
    data = {
        "consents": {"termsConditions": True, "internalMarketing": False},
        "email": f"{random_letters}@outlook.com",
        "username": random_letters,
        "password": "Daapdevontop!",
        "primary_usage": "teacher",
        "primary_usage_type": "SCHOOL",
        "locale": "en"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        token = response.json().get('access_token', 'No token')
        with open("token.txt", "a") as file:
            file.write(f"{data['email']}:{data['password']}:{token}\n")
        with open("credentials.txt", "a") as file:
            file.write(f"{data['email']}:{data['password']}\n")
        print(Fore.GREEN + f"[+] worker {thread_id} genned:" + Style.RESET_ALL + f" {data['email']}:{data['password']}")
    else:
        print(Fore.RED + f"[-] Failed to generate account for {data['email']}" + Style.RESET_ALL)

if __name__ == "__main__":
    threads = int(input("Number of threads: "))
    accounts = int(input("Number of accounts: "))
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(create_account, i) for i in range(accounts)]
        for future in as_completed(futures):
            future.result()
