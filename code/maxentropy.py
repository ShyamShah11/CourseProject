import nltk
import numpy as np
import ast
import sys
import pickle
from sklearn.model_selection import train_test_split

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
max_urls=500

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

#convert data into dictionaries for the classifier
training_dicts = [dict(zip(vocab, vector)) for vector in feature_vectors]
toks = [(training_dict, labels[i]) for i, training_dict in enumerate(training_dicts)]

#create the training and test data
X_train, X_test, y_train, y_test = train_test_split(toks, labels, test_size=0.4, random_state=0)

#create the model and test it
predicted_labels=[]
classifier=nltk.MaxentClassifier.train(X_train, 'GIS', trace = 0, max_iter = 100)

#save the model
with open(model_file, 'wb') as f:
    pickle.dump(classifier, f)

for point in X_test:
    predicted_labels.append(classifier.classify(point[0]))

print("Number of mislabeled points: %d, total points tested: %d"% (sum([predicted_labels[i]!=y_test[i] for i in range(len(y_test))]), len(y_test)))
