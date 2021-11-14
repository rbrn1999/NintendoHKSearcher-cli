from bs4 import BeautifulSoup 
import requests, locale

def HKDtoTWD(amount):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From=HKD&To=TWD"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    twd = soup.select('p[class*="result__BigRate"]')[0].get_text().split()[0].replace(',','')
    twd = int(float(twd))
    return twd


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
locale.setlocale(locale.LC_ALL, 'en_US')

url = "https://store.nintendo.com.hk/catalogsearch/result/?q="
searchTerm = input("search: ")
url = url + searchTerm
page = requests.get(url, headers=headers)
ns_soup = BeautifulSoup(page.content, 'lxml')

game = (ns_soup.find('div', class_="category-product-item"))
if game is None:
    print("no search result")
    exit();

link = game.find('a', href=True)
title = game.find('a', class_="category-product-item-title-link").get_text().lstrip().rstrip()
price = game.find('span', class_="price").get_text()
releaseDate = game.find('div', class_="category-product-item-released").get_text()
releaseDate = releaseDate.split()[-1]
hkd = float(price.lstrip("HKD "))
twd = locale.format_string("%d", HKDtoTWD(hkd), grouping=True)

print("top result:\n")
print(title + '\n')
if hkd != 0:
    print("Price: " + price)
    print(f"(is equivalent to about TWD {twd})")
else:
    print("price: FREE")
print("release date: " + releaseDate)
print("link: " + link['href'])
