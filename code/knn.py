from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import sys
import numpy as np
import ast
import pickle
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
positive_file=sys.path[0] + "\data\positive"
negative_file=sys.path[0] + "\data\\negative"
term_frequency_file=sys.path[0] + "\data\\term_frequency"
feature_vector_file=sys.path[0]+"\data\\feature_vectors"
model_file=sys.path[0]+"\models\knn"
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

#reshape and convert data into numpy matrices
feature_vectors=np.array(feature_vectors)
labels=np.array(labels)

#create the training and test data
X_train, X_test, y_train, y_test = train_test_split(feature_vectors, labels, test_size=0.4, random_state=0)

#create the model and test it
neigh=KNeighborsClassifier(n_neighbors=11, weights='distance')
neigh.fit(X_train,y_train)
#save the model
with open(model_file, 'wb') as f:
    pickle.dump(neigh, f)
y_pred = neigh.predict(X_test)
print("k=%d: Number of mislabeled points: %d, total points tested: %d"% (11, (y_test != y_pred).sum(), y_test.shape[0]))

"""
with uniform weights:
k=2: Number of mislabeled points: 117, total points tested: 400
k=3: Number of mislabeled points: 65, total points tested: 400
k=4: Number of mislabeled points: 68, total points tested: 400
k=5: Number of mislabeled points: 64, total points tested: 400
k=6: Number of mislabeled points: 65, total points tested: 400
k=7: Number of mislabeled points: 68, total points tested: 400
k=8: Number of mislabeled points: 60, total points tested: 400
k=9: Number of mislabeled points: 63, total points tested: 400
k=10: Number of mislabeled points: 65, total points tested: 400
k=11: Number of mislabeled points: 61, total points tested: 400
k=12: Number of mislabeled points: 66, total points tested: 400
k=13: Number of mislabeled points: 69, total points tested: 400
k=14: Number of mislabeled points: 71, total points tested: 400
k=15: Number of mislabeled points: 74, total points tested: 400
k=16: Number of mislabeled points: 83, total points tested: 400


with distance weights:
k=2: Number of mislabeled points: 116, total points tested: 400
k=3: Number of mislabeled points: 63, total points tested: 400
k=4: Number of mislabeled points: 64, total points tested: 400
k=5: Number of mislabeled points: 62, total points tested: 400
k=6: Number of mislabeled points: 62, total points tested: 400
k=7: Number of mislabeled points: 63, total points tested: 400
k=8: Number of mislabeled points: 56, total points tested: 400
k=9: Number of mislabeled points: 56, total points tested: 400
k=10: Number of mislabeled points: 56, total points tested: 400
k=11: Number of mislabeled points: 48, total points tested: 400 <-
k=12: Number of mislabeled points: 57, total points tested: 400
k=13: Number of mislabeled points: 57, total points tested: 400
k=14: Number of mislabeled points: 58, total points tested: 400
k=15: Number of mislabeled points: 59, total points tested: 400
k=16: Number of mislabeled points: 60, total points tested: 400

with distance weights and l1:
k=2: Number of mislabeled points: 58, total points tested: 400
k=3: Number of mislabeled points: 59, total points tested: 400
k=4: Number of mislabeled points: 58, total points tested: 400
k=5: Number of mislabeled points: 61, total points tested: 400
k=6: Number of mislabeled points: 61, total points tested: 400
k=7: Number of mislabeled points: 63, total points tested: 400
k=8: Number of mislabeled points: 61, total points tested: 400
k=9: Number of mislabeled points: 64, total points tested: 400
k=10: Number of mislabeled points: 62, total points tested: 400
k=11: Number of mislabeled points: 66, total points tested: 400
k=12: Number of mislabeled points: 65, total points tested: 400
k=13: Number of mislabeled points: 64, total points tested: 400
k=14: Number of mislabeled points: 65, total points tested: 400
k=15: Number of mislabeled points: 66, total points tested: 400


Kept all the parameters at their default.
I wasn't working with much data so I didn't change the algorithm, assuming it automatically chose brute each time


"""