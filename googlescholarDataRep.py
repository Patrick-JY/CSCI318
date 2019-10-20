import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

import ast
import glob, os
import time
import json
import scipy.stats as stats
from pandas.plotting import table
from textwrap import wrap


punctuations = [".", ",", "?", "!", "'", '"', ":", ";", "...", "-", "--", "---", "(", ")", "[", "]"]
punctuationsName = ["Period", "Comma", "QuestionMark",
                    "Exclamation", "Apostrophe", "Quotation",
                    "Colon", "Semicolon", "Ellipsis", "Hyphen",
                    "EnDash", "EmDash", "LeftParentheses", "RightParentheses",
                    "LeftSquareBracket", "RightSquareBracket"]

def howManyHyphens(title):
    return title.count('-');

def placeinLengthList(titleLength,titleLengthList,hyphenCount,lengthTotalAmountofPapers,citeCount):
    if titleLength > 150:
        titleLengthList[hyphenCount][6] += citeCount
        lengthTotalAmountofPapers[hyphenCount][6]+= 1
    elif titleLength > 125:
        titleLengthList[hyphenCount][5] += citeCount
        lengthTotalAmountofPapers[hyphenCount][5]+= 1
    elif titleLength > 100:
        titleLengthList[hyphenCount][4] += citeCount
        lengthTotalAmountofPapers[hyphenCount][4]+= 1
    elif titleLength > 75:
        titleLengthList[hyphenCount][3] += citeCount
        lengthTotalAmountofPapers[hyphenCount][3]+= 1
    elif titleLength > 50:
        titleLengthList[hyphenCount][2] += citeCount
        lengthTotalAmountofPapers[hyphenCount][2]+= 1
    elif titleLength > 25:
        titleLengthList[hyphenCount][1] += citeCount
        lengthTotalAmountofPapers[hyphenCount][1]+= 1
    else:
        titleLengthList[hyphenCount][0] += citeCount
        lengthTotalAmountofPapers[hyphenCount][0]+= 1

def splitFileByNLine(filename, N,citationCount,articleCount,hyphenNull,hyphenOne,hyphenTwo,hyphenThree,hyphenFour,hyphenFive,articleUpdated,totaltitleLengthList,hyphenCountTitleLengthCiteCount,lengthTotalAmountofPapers):
    counter = 0;
    op = ''
    
    with open(filename,'r',encoding='utf-8') as fileToSplit:
        print("opened")
        for line in fileToSplit:
            item_dict = json.loads(line)
            
            if len(item_dict['outCitations']) == 0:
                continue

            #add count for each punctuation in the list
            
            
            bib = {}
            item_dict["bib"] = bib
            item_dict["bib"]["title"] = item_dict["title"]
            
            item_dict['citedby'] = len(item_dict['outCitations'])
            
            #dictobjects.append(item_dict)
            x = item_dict
            if "citedby" in x:
                    if "bib" in x and x["citedby"] > 10:
                        if "title" in x["bib"]:
                            hyphenCount = howManyHyphens(x["bib"]["title"])
                            titleLength = len(x["bib"]["title"])
                            if(hyphenCount == 0):
                                
                                citationCount[0] += x["citedby"]
                                articleCount[0] += 1
                                hyphenNull.append(x["citedby"])
                                articleUpdated[0] = True
                                totaltitleLengthList[0] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,0,lengthTotalAmountofPapers,x["citedby"])
                                
                                
                            elif(hyphenCount == 1):
                                citationCount[1] += x["citedby"]
                                articleCount[1] += 1
                                hyphenOne.append(x["citedby"])
                                articleUpdated[1] = True
                                totaltitleLengthList[1] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,1,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 2):
                                citationCount[2] += x["citedby"]
                                articleCount[2] += 1
                                hyphenTwo.append(x["citedby"])
                                articleUpdated[2] = True
                                totaltitleLengthList[2] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,2,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 3):
                                citationCount[3] += x["citedby"]
                                articleCount[3] += 1
                                hyphenThree.append(x["citedby"])
                                articleUpdated[3] = True
                                totaltitleLengthList[3] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,3,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 4):
                                citationCount[4] += x["citedby"]
                                articleCount[4] += 1
                                articleUpdated[4] = True
                                hyphenFour.append(x["citedby"])
                                totaltitleLengthList[4] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,4,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount >= 5):
                                citationCount[5] += x["citedby"]
                                articleCount[5] += 1
                                hyphenFive.append(x["citedby"])
                                articleUpdated[5] = True
                                totaltitleLengthList[5] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,5,lengthTotalAmountofPapers,x["citedby"])

            

            counter += 1
            if (counter % 10000  == 0):
                print(counter)
            
            if counter == N:
                break

    fileToSplit.close()







def main():
    

    objects = ('0','1','2','3','4','>4');
    y_pos = np.arange(len(objects))
    citationCount = [0,0,0,0,0,0]
    articleCount = [0,0,0,0,0,0]
    meanCitationCount = [0,0,0,0,0,0]
    hyphenNull = []
    hyphenOne = []
    hyphenTwo = []
    hyphenThree = []
    hyphenFour = []
    hyphenFive = []
    filelist = []
    prevfilelist = []
    totaltitleLengthList = [0,0,0,0,0,0]
    meanTitleLengthList = [0,0,0,0,0,0]
    #DatasetOption = "Google"
    DatasetOption = "Semantic"
    puncOption = 9

    ## Hyphen Title counts for the ranges 0-25, 25-50 , 50-75, 75-100, 100-125, 125-150, 150-max
    f5List0 = [0,0,0,0,0,0,0]
    f5List1 = [0,0,0,0,0,0,0]
    f5List2 = [0,0,0,0,0,0,0]
    f5List3 = [0,0,0,0,0,0,0]
    f5List4 = [0,0,0,0,0,0,0]
    f5List5 = [0,0,0,0,0,0,0]
    hyphenCountTitleLengthCiteCount = [f5List0,f5List1,f5List2,f5List3,f5List4,f5List5]
    lengthTotalAmountofPapers = [f5List0.copy(),f5List1.copy(),f5List2.copy(),f5List3.copy(),f5List4.copy(),f5List5.copy()]
    
    
    


    
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
    f2 = plt.figure(2)
        
    plt.bar(y_pos,citationCount,align = 'center', alpha = 0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('Mean Citation Count')
    plt.title(DatasetOption + ' Scholar: Mean Citation Count and ' + punctuationsName[puncOption])


   



    
    articleUpdated = [False,False,False,False,False,False]
    

    if DatasetOption == "Google":
        for file in glob.glob("GoogleScholar Data/*.txt"):
            if file not in filelist:
                filelist.append(file)
                
        

        
        newfilelist = list(set(filelist) - set(prevfilelist))
        
        for fileObj in newfilelist:
            
            file = fileObj
            dictobjects = []
            dic_list_op = open(file,'r',encoding = "utf8")
            dic_list_str = dic_list_op.read()
            dic_list_op.close()

            dic_list_split_arr = dic_list_str.split('\'}{')

            for index,x in zip(range(len(dic_list_split_arr)),dic_list_split_arr): 
                if index != 0 and index != (len(dic_list_split_arr)- 1) :
                    dictobjects.append(ast.literal_eval("{" + x + "'}"))
                    
                elif index == (len(dic_list_split_arr)- 1) :
                
                    dictobjects.append(ast.literal_eval("{" + x))
                else:
                    y = x.split('{',1)[1]
                    
                    dictobjects.append(ast.literal_eval("{" + y + "'}"))
            
                    
            


            for index,x in zip(range(len(dictobjects)),dictobjects):
                
                if "citedby" in x:
                    if "bib" in x and x["citedby"] > 10:
                        if "title" in x["bib"]:
                            hyphenCount = howManyHyphens(x["bib"]["title"])
                            titleLength = len(x["bib"]["title"])
                            if(hyphenCount == 0):
                                
                                citationCount[0] += x["citedby"]
                                articleCount[0] += 1
                                hyphenNull.append(x["citedby"])
                                articleUpdated[0] = True
                                totaltitleLengthList[0] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,0,lengthTotalAmountofPapers,x["citedby"])
                                
                                
                            elif(hyphenCount == 1):
                                citationCount[1] += x["citedby"]
                                articleCount[1] += 1
                                hyphenOne.append(x["citedby"])
                                articleUpdated[1] = True
                                totaltitleLengthList[1] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,1,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 2):
                                citationCount[2] += x["citedby"]
                                articleCount[2] += 1
                                hyphenTwo.append(x["citedby"])
                                articleUpdated[2] = True
                                totaltitleLengthList[2] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,2,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 3):
                                citationCount[3] += x["citedby"]
                                articleCount[3] += 1
                                hyphenThree.append(x["citedby"])
                                articleUpdated[3] = True
                                totaltitleLengthList[3] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,3,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount == 4):
                                citationCount[4] += x["citedby"]
                                articleCount[4] += 1
                                articleUpdated[4] = True
                                hyphenFour.append(x["citedby"])
                                totaltitleLengthList[4] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,4,lengthTotalAmountofPapers,x["citedby"])
                                
                            elif(hyphenCount >= 5):
                                citationCount[5] += x["citedby"]
                                articleCount[5] += 1
                                hyphenFive.append(x["citedby"])
                                articleUpdated[5] = True
                                totaltitleLengthList[5] += titleLength
                                placeinLengthList(titleLength,hyphenCountTitleLengthCiteCount,5,lengthTotalAmountofPapers,x["citedby"])
    elif DatasetOption == "Semantic":
        dictobjects = []
        splitFileByNLine("papers-2017-10-30.json", 2000000,citationCount,articleCount,hyphenNull,hyphenOne,hyphenTwo,hyphenThree,hyphenFour,hyphenFive,
                         articleUpdated,totaltitleLengthList,hyphenCountTitleLengthCiteCount,lengthTotalAmountofPapers)
        newfilelist = []
        newfilelist.append("papers-2017-10-30.json")
        
        
        print("got here")
        
                
                
        




    
    print(*citationCount)
    for num,citeCount in enumerate(citationCount,start=0):
        if(articleCount[num] != 0) and (len(newfilelist) != 0) and articleUpdated[num]:
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
    

   

   
    plt.figure(1)
    the_table = plt.table(cellText=data,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                          loc = "center")
    plt.subplots_adjust(left=0.2,top = 0.8)
    plt.title(DatasetOption + " Scholar Data Description (Columns are " + punctuationsName[puncOption] +  "count)", y = 0.67)
    f1.canvas.draw()
    f1.canvas.flush_events()
    plt.pause(0.05)
    
    


    plt.figure(2)
    f2.clear()
    plt.bar(y_pos,meanCitationCount,align = 'center',color = (0.2, 0.4, 0.6, 0.6))
    plt.bar(y_pos,meanCitationCount,align = 'center', alpha = 0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('Mean Citation Count')
    plt.title("\n".join(wrap(DatasetOption + ' Scholar: Mean Citation Count related to ' + punctuationsName[puncOption] + ' count')))

    
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
        HyphenLabel.append('>4')

    
    countData = hyphenNull + hyphenOne + hyphenTwo + hyphenThree + hyphenFour + hyphenFive
    print('before: ' + str(countData[0]))
    countData = np.log10(countData)
    print('after: ' + str(countData[0]))

    boxData = {punctuationsName[puncOption] + 's':HyphenLabel,'Count':countData}
    
    df = pd.DataFrame(boxData)
    
    print(df)
    
   
    

    
    boxplot = df.boxplot(column ='Count', by = punctuationsName[puncOption] + 's')
    boxplot.set_ylabel("Mean Citation Count (LOG SCALE)")
    boxplot.set_title(DatasetOption + " Scholar")
    print(boxplot)
    
    
    
    plt.pause(0.05)
    f4 = plt.figure(4)
    for num,titlelength in enumerate(totaltitleLengthList,start=0):
        if(articleCount[num] != 0) and (len(newfilelist) != 0) and articleUpdated[num]:
            meanTitleLengthList[num] = titlelength/articleCount[num]

    plt.bar(y_pos,meanTitleLengthList,align = 'center',color = (0.2, 0.4, 0.6, 0.6))
    plt.bar(y_pos,meanTitleLengthList,align = 'center', alpha = 0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('Mean title length')
    plt.title("\n".join(wrap(DatasetOption +
                             ' Scholar: Mean Title length related to ' + punctuationsName[puncOption] + ' count')))

    
    f4.canvas.draw()
    plt.pause(0.05)

    #f5,ax3 = plt.subplots()
##    f5w = 0.3

    f5x = ['0','1','2','3','4','>4']
    valListList = [[],[],[],[],[],[],[]]

    for i in range(7):
        for j in range(6):
            if lengthTotalAmountofPapers[j][i] == 0:
                number = 0
            else:
                number = hyphenCountTitleLengthCiteCount[j][i]/lengthTotalAmountofPapers[j][i]
            valListList[i].append(number)
    
    #valListList[0] = [hyphenCountTitleLengthCiteCount[0][0]/lengthTotalAmountofPapers[0][0]]


    

    f5Data = {'0-25': valListList[0], '25-50': valListList[1], '50-75': valListList[2], '75-100': valListList[3],
              '100-125': valListList[4],'125-150': valListList[5],'150-max': valListList[6] }
    df5 =  pd.DataFrame(f5Data,index = f5x)
    axf5 = df5.plot.bar(rot = 0)
    axf5.set_ylabel("Mean Citation Count")
    axf5.set_xlabel(punctuationsName[puncOption] + " Count")
    axf5.legend(title = "Title Length in Characters")
    axf5.set_title("\n".join(wrap(DatasetOption + " Scholar: Graphs grouped by " + punctuationsName[puncOption] +
                   "count in relation to mean Citation Count")))
    print(df5)
    
        
##    ax3.bar(f5x-0.6,valListList[0],width = 0.2,align = 'center')
##    ax3.bar(f5x-0.4,valListList[1],width = 0.2,align = 'center')
##    ax3.bar(f5x-0.2,valListList[2],width = 0.2,align = 'center')
##    ax3.bar(f5x,valListList[3],width = 0.2,align = 'center')
##    ax3.bar(f5x+0.2,valListList[4],width = 0.2,align = 'center')
##    ax3.bar(f5x+0.4,valListList[5],width = 0.2,align = 'center')
    plt.show()
    plt.pause(0.05)


    f6listlist = [[],[],[],[],[],[]]

    for i in range(6):
        for j in range(7):
            if lengthTotalAmountofPapers[i][j] == 0:
                number = 0
            else:
                number = hyphenCountTitleLengthCiteCount[i][j]/lengthTotalAmountofPapers[i][j]
            f6listlist[i].append(number)

    
    f6x = ['0-25','25-50','50-75','75-100','100-125','125-150','150-max']
    f6Data = {'0':f6listlist[0],'1':f6listlist[1],'2':f6listlist[2],'3':f6listlist[3]
              ,'4':f6listlist[4],'>4':f6listlist[5]}

    df6 = pd.DataFrame(f6Data,index = f6x)
    axf6 = df6.plot.bar(rot = 0)
    axf6.set_ylabel("Mean Citation Count")
    axf6.set_xlabel("Title Length in characters")
    axf6.legend(title = punctuationsName[puncOption] + " Count")
    axf6.set_title("\n".join(wrap(DatasetOption +
                                  " Scholar: Graphs grouped by Title Length in relation to mean Citation Count")))
    plt.show()
    plt.pause(0.05)

    print(np.var(hyphenNull))
    print(np.var(hyphenOne))
    print(stats.ttest_ind(a=hyphenNull,b=hyphenOne,equal_var = False))
    
    pValueData = {'0':[round(stats.ttest_ind(a=hyphenNull,b=hyphenNull,equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenNull,b=hyphenOne,equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenNull,b=hyphenTwo,equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenNull,b=hyphenThree,equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenNull,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenNull,b=hyphenFive, equal_var = False)[1],4)],

                  '1':[round(stats.ttest_ind(a=hyphenOne,b=hyphenNull, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenOne,b=hyphenOne, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenOne,b=hyphenTwo, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenOne,b=hyphenThree, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenOne,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenOne,b=hyphenFive, equal_var = False)[1],4)],

                  '2':[round(stats.ttest_ind(a=hyphenTwo,b=hyphenNull, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenTwo,b=hyphenOne, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenTwo,b=hyphenTwo, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenTwo,b=hyphenThree, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenTwo,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenTwo,b=hyphenFive, equal_var = False)[1],4)],

                  '3':[round(stats.ttest_ind(a=hyphenThree,b=hyphenNull, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenThree,b=hyphenOne, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenThree,b=hyphenTwo, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenThree,b=hyphenThree, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenThree,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenThree,b=hyphenFive, equal_var = False)[1],4)],
                  
                  '4':[round(stats.ttest_ind(a=hyphenFour,b=hyphenNull, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFour,b=hyphenOne, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFour,b=hyphenTwo, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFour,b=hyphenThree, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFour,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFour,b=hyphenFive, equal_var = False)[1],4)],
                  
                  '>4':[round(stats.ttest_ind(a=hyphenFive,b=hyphenNull, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFive,b=hyphenOne, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFive,b=hyphenTwo, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFive,b=hyphenThree, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFive,b=hyphenFour, equal_var = False)[1],4),
                       round(stats.ttest_ind(a=hyphenFive,b=hyphenFive, equal_var = False)[1],4)]}

    pdataFrame = pd.DataFrame(pValueData,index = ['0','1','2','3','4','>4'])
    print(pdataFrame)
    f7 = plt.figure(7)
    ax7 = plt.subplot(111, frame_on = False)
    ax7.xaxis.set_visible(False)
    ax7.yaxis.set_visible(False)
    ax7.set_title("\n".join(wrap(DatasetOption + " Scholar: p values when comparing samples of papers based on "
                  + punctuationsName[puncOption] + " count")),loc = "center",y = 0.7)
    table(ax7,pdataFrame,loc = "center")


    
    
    
    prevfilelist = filelist.copy()

        

main()




