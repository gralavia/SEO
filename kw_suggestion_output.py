
from bs4 import BeautifulSoup
import requests
import jieba.analyse
from collections import Counter
from googlesearch import search
import pandas as pd
from collections import defaultdict


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
query = input("please enter keyword:")
all_keywords = []
article2 = ""
article3 = ""
article4 = ""
article5 = ""
article6 = ""

for url in search(query, num=10, stop=10, pause=2.0, lang="zh-TW"):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    for h1 in soup.find_all('h1'):
        article1 = h1.text
    if soup.find_all('h2'):
        for h2 in soup.find_all('h2'):
            article2 = h2.text
    if soup.find_all('h3'):
        for h3 in soup.find_all('h3'):
            article3 = h3.text
    if soup.find_all('h4'):
        for h4 in soup.find_all('h4'):
            article4 = h4.text
    if soup.find_all('h5'):
        for h5 in soup.find_all('h5'):
            article5 = h5.text
    if soup.find_all('h6'):
        for h6 in soup.find_all('h6'):
            article6 = h6.text


    keyword_list = []
    for x1, w in jieba.analyse.extract_tags(article1, withWeight=True):
        keyword_list.append(x1)

    for x2, w in jieba.analyse.extract_tags(article2, withWeight=True):
        keyword_list.append(x2)

    for x3, w in jieba.analyse.extract_tags(article3, withWeight=True):
        keyword_list.append(x3)

    for x4, w in jieba.analyse.extract_tags(article4, withWeight=True):
        keyword_list.append(x4)

    for x5, w in jieba.analyse.extract_tags(article5, withWeight=True):
        keyword_list.append(x5)

    for x6, w in jieba.analyse.extract_tags(article6, withWeight=True):
        keyword_list.append(x6)


    all_keywords += keyword_list

top_keywords = Counter(all_keywords).most_common(10)
print("Top 10 keywords: ", top_keywords)

hash_table = defaultdict(list)

for url in search(query, num=10, stop=10, pause=2.0, lang="zh-TW"):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    for i in range(1,7):
        for heading in soup.find_all(f'h{i}'):
            sentence = heading.text.strip()
            for keyword, _ in top_keywords:
                if keyword in sentence:
                    hash_table[keyword].append(sentence)
                    print(sentence)
                    break

column_names = [keyword for keyword, _ in top_keywords]
df = pd.DataFrame(columns=column_names)

for keyword in column_names:
    values = hash_table[keyword][:10]  # Get up to 10 for the keyword
    values += [''] * (10 - len(values))  # Pad with empty strings if fewer than 10 
    df[keyword] = values

df.to_excel('output.xlsx', index=False)
