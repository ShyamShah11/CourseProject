import nltk
import numpy as np
import ast
import sys
import pickle
from sklearn.model_selection import train_test_split

max_urls=500
if len(sys.argv) >= 2: #a different number of urls to use was passed
    try:
        max_urls=int(sys.argv[1])
        if max_urls<500:
            print ("Please use more than 500 samples")
            exit()
    except ValueError:
        print ("Please pass a valid number of URLs")
        exit()

print ("Using a total of %d URLs to train"% (max_urls*2))

feature_vectors=[]
labels=[]
term_frequency=[]
vocab=[]
positive_file=sys.path[0] + "\data\positive"
negative_file=sys.path[0] + "\data\\negative"
term_frequency_file=sys.path[0] + "\data\\term_frequency"
feature_vector_file=sys.path[0]+"\data\\feature_vectors"
vocab_file=sys.path[0]+"\data\\vocabulary"
model_file=sys.path[0]+"\models\maxentropy"
num_positive=0
num_negative=0

#create a term frequency vector
#if we have already written to the file, just need to read it
with open(term_frequency_file, 'r', encoding="utf-8") as f:
    lines=f.readlines()
    for line in lines:
        term_frequency.append(int(line.strip()))

#create the feature vectors 
#if we have already written to the file, just need to read it
with open(feature_vector_file, 'r', encoding="utf-8") as f:
    lines=f.readlines()
    for line in lines:
        feature_vectors.append(ast.literal_eval(line))
labels=[1]*max_urls+[0]*max_urls

#read the vocabulary from the file as well
with open(vocab_file, 'r', encoding="utf-8") as f:
    vocab=f.readlines()
    vocab=[word.strip() for word in vocab]
word_vectors=[]
#need to get our data in a different form. instead of feature vectors, we want a dictionary of all words that exist in a doc
for fv in feature_vectors:
    #getting rid of cs because it skewed the performance while testing. maybe bc it either shows up on every university's url or none of them
    words=[vocab[i] for i, x in enumerate(fv) if x > 0 and vocab[i]!="cs"]
    word_vectors.append(words)

#taken from http://ataspinar.com/2016/05/07/regression-logistic-regression-and-maximum-entropy-part-2-code-examples/
def list_to_dict(words_list):
    return dict([(word, 1) for word in words_list])

#create new data with all data points that still exist
training_set=[(list_to_dict(element), labels[i]) for i, element in enumerate(word_vectors) if len(element)>0]
labels=[element[1] for element in training_set]

#split data and train model
X_train, X_test, y_train, y_test = train_test_split(training_set, labels, test_size=0.4, random_state=0)
classifier = nltk.MaxentClassifier.train(X_train, "GIS", max_iter=100)
#save the model
with open(model_file, 'wb') as f:
    pickle.dump(classifier, f)

#get predictions for all the test data
predicted_labels=[]
for x in X_test:
    prediction=classifier.classify(x[0])
    predicted_labels.append(prediction)

print("Number of mislabeled points: %d, total points tested: %d"% (sum([predicted_labels[i]!=x[1] for i,x in enumerate(X_test)]), len(y_test)))

"""
with GIS algorithm and 100 iterations, mislabelled 32/343 <-
with GIS algorithm and 500 iterations, mislabelled 34/343

with IIS algorithm and 100 iterations, mislabelled 35/343
with IIS algorithm and 500 iterations, mislabelled 33/343
"""
