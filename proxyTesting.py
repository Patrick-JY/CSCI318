from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import sys
import scholarly
import random
import socks

filename = "randomWords.txt";
file = open(filename, "a", encoding="utf-8")
dictionary = {}

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

with open(filename) as f:
    for line in f:
        dictionary[line] = line

url = 'https://httpbin.org/ip'
scholarly.scholarly._PUBSEARCH = '/scholar?hl=en&q={0}'

keywords_count = 0;
while keywords_count < 10000:
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    iterator = 0;
    while iterator < 50:
       proxy = next(proxy_pool)
       print("Request #%d"%iterator)
       try:
          response = requests.get(url,proxies={"http": proxy, "https": proxy})
          print(response.json())

          scholarly.scholarly._SESSION.proxies = {'http' : 'http://' + proxy, 'https' : 'https://' + proxy}
          print(scholarly.scholarly._SESSION.proxies)
          i = 0
          while i < 1000:
              random_word = random.choice(list(dictionary.keys()))
              newFileName = random_word.replace('\n', '') + ".txt"
              newFile = open(newFileName, "w", encoding="utf-8")
              search_query = scholarly.search_pubs_query(random_word)
              #print(next(search_query))
              keywords_count = keywords_count + 1
              j = 0
              while j < 100:
                  newFile.write(str(next(search_query)))
                  print(j)
                  sys.stdout.flush()
                  j = j + 1
              newFile.close()
              i = i + 1
          # proxies = {"http": 'socks5://' + proxy, 'socks5://' + "https": proxy}
          #  scholarly.scholarly.use_proxy(**proxies)
          #  print(next(scholarly.search_author('Steven A. Cholewiak')))
       except StopIteration:
           print("Access denied by Google Scholar")
           iterator = iterator + 1
       except:
           print("Skipping. Connnection error")
           iterator = iterator + 1
    print("End of 50 proxy cycle")
#proxies = {'http' : 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
#scholarly.use_proxy(**proxies)
#s = requests.session()
#s.proxies = proxies
#scholarly.scholarly.use_proxy()
#print(next(scholarly.search_author('Steven A. Cholewiak')))
#r = s.get('http://www.showmemyip.com/')
#print(r.text)