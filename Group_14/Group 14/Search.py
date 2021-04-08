import json
import porter
import math
import time


def search(keystring):
    file = open('index.txt', encoding='gbk')
    js = file.read()
    dicread = json.loads(js)
    file.close()
    N = dicread['N']
    k = 1
    b = 0.75
    avg = dicread['avg_doclen']
    stemmer = porter.PorterStemmer()
    stopwords = set()
    with open('stopwords.txt', 'r') as f:
        for line in f:
            stopwords.add(line.rstrip())

    keystring = keystring.split(None)
    keylist = []
    for value in keystring:
        if value not in stopwords:
            value = stemmer.stem(value)
            value = value.lower()
            keylist.append(value)
    dic_ij = {}
    dic_ni = {}
    for term in keylist:
        dicij = {}
        i = 0
        for id in dicread['house_index_info']:
            if term in dicread['house_index_info'][id]:
                fij = dicread['house_index_info'][id][term]
                dicij[id] = fij
                i = i + 1
                dic_ni[term] = i
            else:
                fij = 0
                dicij[id] = fij
                dic_ni[term] = i
            dic_ij[term] = dicij
    bmij = {}
    for docid in dicread['house_index_info']:
        sim = 0
        for term in keylist:
            fij = dic_ij[term][docid]
            ni = dic_ni[term]
            len = dicread['indoclen'][docid]
            sim = sim + (fij * (1 + k) / (fij + k * (1 - b + ((b * len) / avg)))) * math.log(
                ((N - ni + 0.5) / (ni + 0.5)), 2)
        bmij[docid] = sim
    bmrank = sorted(bmij.items(), key=lambda x: x[1], reverse=True)[0:100]
    # dic_result = {}
    keylist = []
    for key in bmrank:
        keylist.append(key[0])
    return keylist


#start_search = time.time()
#search = search('Dublin')
#end_search = time.time()
#print(search)
#print('evaluation indexing time:', str(end_search - start_search))
