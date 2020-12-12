from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, CategoricalNB, MultinomialNB, ComplementNB
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
model_file=sys.path[0]+"\models\\naivebayes"
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
bnb = BernoulliNB(fit_prior=False)
y_pred = bnb.fit(X_train, y_train).predict(X_test)
#save the model
with open(model_file, 'wb') as f:
    pickle.dump(bnb, f)
print("Number of mislabeled points: %d, total points tested: %d"% ((y_test != y_pred).sum(), y_test.shape[0]))

"""
Gaussian: Number of mislabeled points: 68, total points tested: 400
Bernoulli: Number of mislabeled points: 53, total points tested: 400 <-
Complement: Number of mislabeled points: 86, total points tested: 400
Multinomial: Number of mislabeled points: 206, total points tested: 400

Bernoulli with fit_prior=False: Number of mislabeled points: 51, total points tested: 400
Tried different priors, based on an empirical estimate but since the dataset is split evenly, the uniform prior worked best


"""