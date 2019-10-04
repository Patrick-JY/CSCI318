from random_words import RandomWords
import scholarly
import random
import time
import sys
rw = RandomWords()

filename = "randomWords.txt";
file = open(filename, "a", encoding="utf-8")
dictionary = {}
i = 0;
#count = 0


with open(filename) as f:
    for line in f:
        dictionary[line] = line
        #print(line)
        #i = i + 1
        #print(i)

while i < 10000:
    random_word = random.choice(list(dictionary.keys()))
   # random.replace('\n','')
    newFileName = random_word.replace('\n','') + ".txt"
    newFile = open(newFileName, "w", encoding="utf-8")
    search_query = scholarly.search_pubs_query(random_word)
    j = 0
    while j < 100:
        newFile.write(str(next(search_query)))
        print(j)
        sys.stdout.flush()
        j = j + 1
    newFile.close()
    i = i + 1
#   count = count + 1
#    if count == 3:
#        print("sleeping...")
#        sys.stdout.flush()
#        time.sleep(600)
#        count = 0


#while i < 100000:
#   word = rw.random_word()
#  dictionary[word] = word;
# i = i + 1

#for i in dictionary:
#    file.write(i)
#    file.write("\n")
#    print(dictionary[i])

#len(dictionary)


