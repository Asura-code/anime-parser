from bs4 import BeautifulSoup as bs
import requests
from googletrans import Translator, constants
from pprint import pprint
from functools import lru_cache

def dist(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    curr = range(n + 1)
    for i in range(1, m + 1):
        prev, curr = curr, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = prev[j] + 1, curr[j - 1] + 1, prev[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            curr[j] = min(add, delete, change)
    return curr[n]



with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

s = input()
f = open('db3.txt', encoding='UTF8').readlines()
for i in f:
    if len(i)>1:
        ind = i.index('|')+6
        if dist(i[ind:].lower(), s.lower())<=2:
            z = i[ind:]
            ind = i.index('|')
            q = i[:ind]

url = 'https://anidb.net/anime/'+ q
while ' ' in z:
    z = z.replace(' ', '%20', 1)
link = f"https://bankaikino.ru/onlinekino.html?lol{z}"

page = se.get(url)
soup = bs(page.text,"html.parser")
m = []

m = soup.findAll('span',itemprop='name')
name = m[4].text

m2 = soup.findAll('div', itemprop='description')
desc = m2[0].text

m = soup.findAll('span', itemprop='ratingValue')
rating = m[0].text

print(f"Название: {name}\n"
      f"Рейтинг: {rating}")
translator = Translator()
translation = translator.translate(desc, dest="ru")
print(f"Описание: {translation.text}")
print(f"Смотреть: {link}")