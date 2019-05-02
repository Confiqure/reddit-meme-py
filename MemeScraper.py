from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("https://reddit.com/r/MemeEconomy/")
soup = BeautifulSoup(html, "lxml")
#print(str(soup.prettify()))

# cards = soup.find_all("a", {"class": "data-href-url"})
# for card in cards:
#     print(card.prettify())

for link in soup.find_all("a"):
    print(link)



#print("All Headers:", soup.find_all(True))


