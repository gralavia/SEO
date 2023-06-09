import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from collections import defaultdict
import datetime

# reference : https://blog.christian-schou.dk/how-to-track-the-of-keywords-in-google-using-python/

# Declare request header
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','referer':'https://www.google.com'}

# Pair of kw-url

search_for_domain = {
    'kw1': 'url1',
    'kw2': 'url2',
    'kw3': 'url3',   
}

search_engine = 'https://www.google.com.tw/search?q='

hash_table = defaultdict(list)
for keyword, url in search_for_domain.items():
    target_url = (search_engine + keyword + '&num=100').encode('utf-8')

    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all("div", class_="MjjYud")
    for result in range(0, len(results)):
        domain = urlparse(results[result].find("a").get("href")).netloc
        if (url in domain):
            found = True
            position = result + 1
            print()
            print(f"{keyword} is found at position {position}")
            hash_table[keyword].append(position)
            break
        else:
            found = False

current_date = datetime.datetime.now().strftime('%m%d')
filename = f'output_{current_date}.xlsx'
df = pd.DataFrame(hash_table)
df.to_excel(filename, index=False)

