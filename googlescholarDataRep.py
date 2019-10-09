import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import scholarly
import ast
import glob, os
import time





def howManyHyphens(title):
    return title.count('-');


def main():
    

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
    filelist = []
    prevfilelist = []



    
    #Needed info for figure 1
    data = [[0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0]]
    f1,ax = plt.subplots()
    
    f1.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    columns = ['0','1','2','3','4','>4','Overall']
    rows = ['No of papers','Percentage']
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
    the_table = plt.table(cellText=data,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                              loc = "center")
    plt.subplots_adjust(left=0.2,top = 0.8)
    
    plt.ion()
    
    #Needed info for figure 2
    
    
    while 1:
        time.sleep(10)

        
        for file in glob.glob("Set 3/*.txt"):
            if file not in filelist:
                filelist.append(file)
                
        

        print(prevfilelist)
        newfilelist = list(set(filelist) - set(prevfilelist))
        
        for fileObj in newfilelist:
            
            file = fileObj
            dictobjects = []
            dic_list_op = open(file,'r',encoding = "utf8")
            dic_list_str = dic_list_op.read()
            dic_list_op.close()

            dic_list_split_arr = dic_list_str.split('}{')

            for index,x in zip(range(len(dic_list_split_arr)),dic_list_split_arr): 
                if index != 0 and index != (len(dic_list_split_arr)- 1) :
                    dictobjects.append(ast.literal_eval("{" + x + "}"))
                elif index == (len(dic_list_split_arr)- 1) :
                    dictobjects.append(ast.literal_eval("{" + x))
                else:
                    y = x.split('{',1)[1]
                    dictobjects.append(ast.literal_eval("{" + y + "}"))
            
                    
            


            for index,x in zip(range(len(dictobjects)),dictobjects):
                
                if "citedby" in x:
                    if "bib" in x and x["citedby"] > 100:
                        if "title" in x["bib"]:
                            hyphenCount = howManyHyphens(x["bib"]["title"])
                            if(hyphenCount == 0):
                                citationCount[0] += x["citedby"]
                                articleCount[0] += 1
                                hyphenNull.append(x["citedby"])
                            elif(hyphenCount == 1):
                                citationCount[1] += x["citedby"]
                                articleCount[1] += 1
                                hyphenOne.append(x["citedby"])
                            elif(hyphenCount == 2):
                                citationCount[2] += x["citedby"]
                                articleCount[2] += 1
                                hyphenTwo.append(x["citedby"])
                            elif(hyphenCount == 3):
                                citationCount[3] += x["citedby"]
                                articleCount[3] += 1
                                hyphenThree.append(x["citedby"])
                            elif(hyphenCount == 4):
                                citationCount[4] += x["citedby"]
                                articleCount[4] += 1
                                hyphenFour.append(x["citedby"])
                            elif(hyphenCount >= 5):
                                citationCount[5] += x["citedby"]
                                articleCount[5] += 1
                                hyphenFive.append(x["citedby"])




        meanCitationCount = citationCount
        print(*citationCount)
        for num,citeCount in enumerate(meanCitationCount,start=0):
            if(articleCount[num] != 0):
                meanCitationCount[num] = citeCount/articleCount[num]

        print(*meanCitationCount)
        
        

        

        totalcount = 0
        for x in articleCount:
            totalcount += x
        
        if totalcount == 0:
            totalcount = 1
        
        
        
    ##    data = [[articleCount[0],round(articleCount[0]/totalcount)],
    ##                        [articleCount[1],round(articleCount[1]/totalcount)],[articleCount[2],round(articleCount[2]/totalcount)],
    ##                         [articleCount[3],round(articleCount[3]/totalcount)],[articleCount[4],round(articleCount[4]/totalcount)],
    ##                         [articleCount[5],round(articleCount[5]/totalcount)],[totalcount,100]
    ##                         ]
        data = [[articleCount[0],articleCount[1],articleCount[2],articleCount[3],articleCount[4],articleCount[5],totalcount],
                [round((articleCount[0]/totalcount)*100,2),round((articleCount[1]/totalcount)*100,2) , round((articleCount[2]/totalcount)* 100,2) ,
                 round((articleCount[3]/totalcount) * 100,2)
                 ,round((articleCount[4]/totalcount) * 100,2),
                 round((articleCount[5]/totalcount) * 100,2),100]]
        

       

       
            
        the_table = plt.table(cellText=data,
                          rowLabels=rows,
                          rowColours=colors,
                          colLabels=columns,
                              loc = "center")
        plt.subplots_adjust(left=0.2,top = 0.8)
        
        f1.canvas.draw()
        plt.pause(0.05)
        
        


        f2 = plt.figure(2)
        
        plt.bar(y_pos,citationCount,align = 'center', alpha = 0.5)
        plt.xticks(y_pos,objects)
        plt.ylabel('Mean Citation Count')
        plt.title('Mean Citation Count and Hyphens')
        
        f2.canvas.draw()
        plt.pause(0.05)


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
        plt.pause(0.05)
        f3.canvas.draw()
        prevfilelist = filelist.copy()

        

main()




