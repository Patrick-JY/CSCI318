from random_word import RandomWords
import scholarly
import time

r = RandomWords()
i = 0;
count = 0;

while i < 100:
    random = str(r.get_random_word(hasDictionaryDef="true"))
    print(random)
    filename = random + ".txt";
    file = open(filename, "w", encoding="utf-8")
    search_query = scholarly.search_pubs_query(random)
    j = 0
    while j < 100:
        file.write(str(next(search_query)))
        print(j)
        j = j + 1
    file.close()
    i = i + 1
    count = count + 1
    if count == 5:
        time.sleep(900)
        count = 0
