from urllib.request import urlopen
import json
from json2xml import json2xml, readfromstring
from xml import etree
from itertools import zip_longest
eutil_api_token = ''
eutil_api_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
#db - pubmed, usehistory = y|n
punctuations = [".", ",", "?", "!", "'", '"', ":", ";", "...", "-", "--", "---", "(", ")", "[", "]"]
punctuationsName = ["period", "comma", "questionMark", "exclamation", "apostrophe", "quotation", "colon", "semicolon", "ellipsis", "hyphen", "enDash", "emDash", "leftParentheses", "rightParentheses", "leftSquareBracket", "rightSquareBracket"]

def BasicSearch(database, query, store):
    search_string = 'esearch.fcgi?db=' + database + '&term=' + query + 'usehistory='+store
    final_url = eutil_api_base+search_string
    json_obj = urlopen(final_url)



#db = pubmed, rettype = xml
def SearchWithCitation(database, rettype, query):
    search_string = 'ecitmatch.cgi?db='+ database+ '&rettype='+rettype+'&bdata='+query
    final_url = eutil_api_base + search_string
    xml_result = urlopen(final_url)


#db = protein, idList = 6678417,9507199,28558982,28558984,28558988,28558990
def BasicDownloadDocumentSum(database,idList):
    search_string = 'esummary.fcgi?db='+database+'&id='+idList
    final_url = eutil_api_base + search_string
    xml_result = urlopen(final_url)

def BasicSearchSemanticScholar(S2PaperId, DOI, ArXivId):
    search_string = 'http://api.semanticscholar.org/v1/paper'
    if S2PaperId != '' :
        search_string += '/' + str(S2PaperId)
    if DOI != '':
        search_string += '/' + str(DOI)
    if ArXivId != '':
        search_string += '/' + str(ArXivId)
    search_result = urlopen(search_string)

def getOutCitation():

    return

#split large json file by N line then transform them into xml
def splitFileByNLine(filename, N):
    counter = 0;
    op = ''
    with open(filename,'r',encoding='utf-8') as fileToSplit:
        for line in fileToSplit:
            item_dict = json.loads(line)

            if len(item_dict['outCitations']) == 0:
                continue

            #add count for each punctuation in the list
            PunIndex = 0
            totalPunctuationCount = 0
            for pun in punctuations:
                punC = item_dict['title'].count(pun)
                item_dict[punctuationsName[PunIndex]+"Count"] = punC
                totalPunctuationCount += punC
                PunIndex += 1

            item_dict['CitedBy'] = len(item_dict['outCitations'])
            item_dict['totalPun'] = totalPunctuationCount
            item_json = json.dumps(item_dict)
            item_xml = StringJsonToXml(item_json)
            if counter % N == 0 and counter != 0:
                with open(str(counter) + '.xml', 'w', encoding='utf-8') as opf:
                    opf.write(op)
                    opf.close()
                    op = '' + item_xml
                    counter += 1

            else:
                op += item_xml
                counter += 1

    fileToSplit.close()



#read a item_json theen turn them into xml only work for 1 json object
def StringJsonToXml(item_json):
    data = readfromstring(item_json)
    item_xml = json2xml.Json2xml(data).to_xml()
    return item_xml


splitFileByNLine("papers-2017-10-30-sample.json", 1000)

