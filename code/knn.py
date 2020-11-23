from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import sys
import numpy as np
import ast

feature_vectors=[]
labels=[]
term_frequency=[]
positive_file=sys.path[0] + "\data\positive"
negative_file=sys.path[0] + "\data\\negative"
term_frequency_file=sys.path[0] + "\data\\term_frequency"
feature_vector_file=sys.path[0]+"\data\\feature_vectors"
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

#reshape and convert data into numpy matrices
feature_vectors=np.array(feature_vectors)
labels=np.array(labels)

#create the training and test data
X_train, X_test, y_train, y_test = train_test_split(feature_vectors, labels, test_size=0.4, random_state=0)

#create the model and test it
neigh=KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train,y_train)
y_pred = neigh.predict(X_test)
print("Number of mislabeled points: %d, total points tested: %d"% ((y_test != y_pred).sum(), y_test.shape[0]))