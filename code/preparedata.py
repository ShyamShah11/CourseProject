import re
import sys
import numpy as np
import ast
import enchant

vocab=[]
feature_vectors=[]
labels=[]
term_frequency=[]
positive_file=sys.path[0] + "\data\positive"
negative_file=sys.path[0] + "\data\\negative"
term_frequency_file=sys.path[0] + "\data\\term_frequency"
feature_vector_file=sys.path[0]+"\data\\feature_vectors"
num_positive=0
num_negative=0
max_urls=500 #the number of positive and negative urls being used

"""
the datasets I am using are only links taken from university websites. 
they probably have abbreviations of the university name which woudn't be an english word.
they faculty links also probably have the faculty members name or some kind of alias 
which wouldn't be an english word. 
ExpertSearch will probably be crawling university pages to gather URLs

the idea is that if we only look at english words, we can simplify our data by a lot without losing much
in terms of performance since every link will have an abbreviation of the university name and
full names/aliases will likely only occur for one person. 
I am going to test this out further but am leaning towards using this
"""
def getVocab(file_name):
    #store the entire file as a string so we can split it on non alphabet characters
    global vocab
    with open(file_name, 'r', encoding="utf-8") as f:
        tempVocab = f.read().replace('\n','-')
        f.close()
    tempVocab=re.split('[^a-z]', tempVocab)
    #only count english words as tokens
    d=enchant.Dict("en_US") 
    for word in tempVocab:
        try: 
            if (d.check(word)):
                vocab.append(word)
        except:
            pass

def getFeatureVectors(file_name, label):
    global feature_vectors
    global labels
    global term_frequency
    global feature_vector_file
    global num_negative
    global num_positive
    global max_urls
    w=open(feature_vector_file,'a', encoding="utf-8")
    with open(file_name, 'r', encoding="utf-8") as f:
        for i, url in enumerate(f):
            if (i >= max_urls):
                break
            #first get the tokens in the URL
            tokens = re.split('[^a-z]', url)
            #create the feature vector with IDF weighting (kind of)
            feature_vector=[tokens.count(word)/term_frequency[index] for index,word in enumerate(vocab)]
            #stream the feature vectors to the file to avoid needing to store a lot in memory
            w.write(str(feature_vector))
            w.write("\n")
            if (i % 50 == 0):
                print ("generated feature vector for %d urls"% i)
        f.close()
    w.close()


def saveToFile(file_name, values):
    with open(sys.path[0] + "\data\\term_frequency", 'a', encoding="utf-8") as f:
        for i, term in enumerate(values):
            f.write(str(term) + "\n")



#get vocabulary from both datasets
getVocab(positive_file)
getVocab(negative_file)

#remove duplicates
vocabWithDup = vocab.copy()
vocab = list(dict.fromkeys(vocab))

#remove redundancies
try:
    vocab.remove('http')
    vocab.remove('https')
    vocab.remove('')
except:
    pass

#create a term frequency vector
num_features = len(vocab)
"""
#run this once to create and save it since it takes a while
for i, word in enumerate(vocab):
    term_frequency.append(vocabWithDup.count(word))
    if (i%100==0): #periodically write to the file
        saveToFile("\data\\term_frequency", term_frequency)
        term_frequency=[]

saveToFile("\data\\term_frequency", term_frequency)
term_frequency=[]
"""

#read the entire term frequency list for the feature vectors
with open(term_frequency_file, 'r', encoding="utf-8") as f:
    lines=f.readlines()
    for line in lines:
        term_frequency.append(int(line.strip()))


#create the feature vectors 

#run this once to generate the feature vectors and save it since it takes a while
getFeatureVectors(positive_file, 1)
getFeatureVectors(negative_file, 0)
feature_vectors=[]
