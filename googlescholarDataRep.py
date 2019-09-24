import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import scholarly





def howManyHyphens(title):
    return title.count('-');


def main():
    search_query = scholarly.search_pubs_query('Perception');

    objects = ('0','1','2','3','4','>4');
    y_pos = np.arange(len(objects))
    citationCount = [0,0,0,0,0,0]
    articleCount = [0,0,0,0,0,0]
    hyphenNull = []
    hyphenOne = []
    hyphenTwo = []
    hyphenThree = []
    hyphenFour = []
    hyphenFive = []
    for index,x in zip(range(100),search_query):
        print(x)
        hyphenCount = howManyHyphens(x.bib["title"])
        if(hyphenCount == 0):
            citationCount[0] += x.citedby
            articleCount[0] += 1
            hyphenNull.append(x.citedby)
        elif(hyphenCount == 1):
            citationCount[1] += x.citedby
            articleCount[1] += 1
            hyphenOne.append(x.citedby)
        elif(hyphenCount == 2):
            citationCount[2] += x.citedby
            articleCount[2] += 1
            hyphenTwo.append(x.citedby)
        elif(hyphenCount == 3):
            citationCount[3] += x.citedby
            articleCount[3] += 1
            hyphenThree.append(x.citedby)
        elif(hyphenCount == 4):
            citationCount[4] += x.citedby
            articleCount[4] += 1
            hyphenFour.append(x.citedby)
        elif(hyphenCount >= 5):
            citationCount[5] += x.citedby
            articleCount[5] += 1
            hyphenFive.append(x.citedby)


    meanCitationCount = citationCount
    print(*citationCount)
    for num,citeCount in enumerate(meanCitationCount,start=0):
        if(articleCount[num] != 0):
            meanCitationCount[num] = citeCount/articleCount[num]

    print(*meanCitationCount)
    
    

    

    totalcount = 0
    for x in articleCount:
        totalcount += x
    

    
    f1,ax = plt.subplots()
    columns = ['No. of Hyphens','0','1','2','3','4','>4','Overall']
    rows = ['No of papers','Percentage']
    data = [[articleCount[0],articleCount[0]/totalcount],
                        [articleCount[1],articleCount[1]/totalcount],[articleCount[2],articleCount[2]/totalcount],
                         [articleCount[3],articleCount[3]/totalcount],[articleCount[4],articleCount[4]/totalcount],
                         [articleCount[5],articleCount[5]/totalcount],[totalcount,100]
                         ]
    data = [[articleCount[0],articleCount[1],articleCount[2],articleCount[3],articleCount[4],articleCount[5],totalcount],
            [articleCount[0]/totalcount,articleCount[1]/totalcount , articleCount[2]/totalcount, articleCount[3]/totalcount , articleCount[4]/totalcount, articleCount[5]/totalcount,100]]
    

    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))


    f1.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

   
        
    the_table = plt.table(cellText=data,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                          loc = "center")
    plt.subplots_adjust(left=0.2,top = 0.8)
    f1.show()
    
    


    
    f2 = plt.figure(2)
    
    plt.bar(y_pos,citationCount,align = 'center', alpha = 0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('Mean Citation Count')
    plt.title('Mean Citation Count and Hyphens')

    f2.show()


    HyphenLabel = []

    for x in hyphenNull:
        HyphenLabel.append('0')

    for x in hyphenOne:
        HyphenLabel.append('1')

    for x in hyphenTwo:
        HyphenLabel.append('2')

    for x in hyphenThree:
        HyphenLabel.append('3')

    for x in hyphenFour:
        HyphenLabel.append('4')

    for x in hyphenFive:
        HyphenLabel.append('5')

    countData = hyphenNull + hyphenOne + hyphenTwo + hyphenThree + hyphenFour + hyphenFive

    boxData = {'Hyphens':HyphenLabel,'Count':countData}
    
    df = pd.DataFrame(boxData)
    print(df)
    

    
    df.boxplot(column ='Count', by ='Hyphens')
    f3 = plt.figure(3)
    f3.show()
    

main()




