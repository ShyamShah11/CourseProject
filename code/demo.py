import pickle
import sys
import re
import nltk
import numpy as np

#check that you passed something to classify
try:
    urls = sys.argv[1].split(",")
except IndexError:
    print ("Please pass comma delimited URLs to classify")
    exit()
print (urls)

maxent_filename = sys.path[0]+"\models\maxentropy"
knn_filename = sys.path[0]+"\models\knn"
naivebayes_filename = sys.path[0]+"\models\\naivebayes"
vocab_filename = sys.path[0]+"\data\\vocabulary"
termfreq_filename = sys.path[0]+"\data\\term_frequency"

def getClassifier(model_name):
    #load the maxent classifier model
    print("Loading " + model_name.split("\\")[-1] + " classifier...", end=" ")
    f = open(model_name, "rb")
    classifier = pickle.load(f)
    f.close()
    print("Done")
    return classifier

#taken from http://ataspinar.com/2016/05/07/regression-logistic-regression-and-maximum-entropy-part-2-code-examples/
def list_to_dict(words_list):
    return dict([(word, 1) for word in words_list])

#first load in the vocabulary and term frequency
print("Loading vocabulary...", end=" ")
f = open(vocab_filename, "r")
vocab=f.readlines()
vocab=[word.strip() for word in vocab]
f.close()
print("Done")
print("Loading term frequencies...", end=" ")
f = open(termfreq_filename, "r")
term_frequency=f.readlines()
f.close()
term_frequency=[int(line.strip()) for line in term_frequency]
print("Done")
    
#convert urls into feature vector
print("Converting URLs to feature vectors...", end=" ")
tokens=[re.split('[^a-z]', url) for url in urls]
feature_vectors=[]
for token in tokens:
    feature_vectors.append([token.count(word)/term_frequency[index] for index,word in enumerate(vocab)])
print("Done")

#make predictions using the maxent classifier
#we first need to get the feature vector into the dictionary form used for this model
word_vectors=[]
for fv in feature_vectors:
    #getting rid of cs we did that for this model
    words=[vocab[i] for i, x in enumerate(fv) if x > 0 and vocab[i]!="cs"]
    word_vectors.append(words)
maxent_vectors=[list_to_dict(element) for i, element in enumerate(word_vectors) if len(element)>0]
maxent_classifier=getClassifier(maxent_filename)
for i, fv in enumerate(maxent_vectors):
    print ("%s was labelled as %s"% (urls[i], "positive" if (maxent_classifier.classify(fv)==1) else "negative"))
    #1 is faculty, 0 is not faculty

#make predictions using the knn classifier
knn_classifier=getClassifier(knn_filename)
for i, fv in enumerate(feature_vectors):
    print ("%s was labelled as %s"% (urls[i], "positive" if (knn_classifier.predict(np.array(fv).reshape(1,-1))==1) else "negative"))

#make predictions using the naive bayes classifier
naivebayes_classifier=getClassifier(naivebayes_filename)
for i, fv in enumerate(feature_vectors):
    print ("%s was labelled as %s"% (urls[i], "positive" if (naivebayes_classifier.predict(np.array(fv).reshape(1,-1))==1) else "negative"))

