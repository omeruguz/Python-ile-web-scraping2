import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=16&filter_in_stock=1&filter_in_stock=1&limit=100"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

fiyatlar = []
yazarlar = []
yayinlar = []

pricenew = soup.find_all("div", {"class": "price-new"})
authors = soup.find_all("div", {"class": "author compact ellipsis"})
publishers = soup.find_all("div", {"class": "publisher"})
book_list = soup.find_all("div", {"class": "name ellipsis"})

for price in pricenew:
    fiyat = price.find("span", {"class": "value"}).text.strip().replace(",", ".") + " TL"
    fiyatlar.append(fiyat)

for author in authors:
    yazar = author.find("a", {"class": "alt"}).text.strip()
    yazarlar.append(yazar)

for publisher in publishers:
    yayin = publisher.find("a", {"class": "alt"}).text.strip()
    yayinlar.append(yayin)

kitaplar = []
for i, book in enumerate(book_list):
    title = book.find("span").text.strip()
    link = book.find("a").get("href")
    kitap = {
        "ID": i + 1,
        "Kitap Adı": title,
        "Yazar": yazarlar[i],
        "Yayıncı": yayinlar[i],
        "Bağlantı URL": link,
        "Fiyat": fiyatlar[i]
    }
    kitaplar.append(kitap)


client = MongoClient("mongodb://localhost:27017/")
db = client["smartmaple"]
collection = db["kitapyurdu"]
collection.insert_many(kitaplar)
print("işlem tamamlandı")
