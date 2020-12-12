# Instructions
Video demo available [here](https://drive.google.com/file/d/1GHTCM-BtEnMNwwzLdWTJBcKEtZyAQ-xz/view?usp=sharing). it is also included as a part of this repsitory as demo.mp4.

## Setup
This was developed and tested using Python 3.7.6. After cloning this repository, download all of the external packages used in the code by running `pip install -r requirements.txt`. Note that I use some packages that are downloaded by default such as sys and ast too. All of the files ran are in this folder (code) so make sure to navigate to it before running any of the lines below.

## Test the models
This repository comes with some pre-trained models. There are two ways to test them. 
1. Pass a list of comma delimited urls as an argument. Since they're being passed as an argument, make sure there are no spaces between the urls. For example, `python demo.py url1,url2`
2. Create a txt file with urls (one per line) and pass the text file as an argument like this `python demo.py urls.txt`

You will then see a couple of messages about different components being loaded, followed by lines like `url1 was classified was labelled as negative/positive`. A positive label means that the model thinks that it is a faculty URL and negative means the opposite.

## Retrain the models
You can retrain all 3 of the models. You will first need to run preparedata.py to generate the feature vectors for them with a command like `python preparedata.py 1000`. The numerical argument is the number of positive and negative samples to prepare and must be greater than 500 which is the default. This is the most time consuming part of retraining the models. 

The code to train them are in the knn.py, maxentropy.py, and naivebayes.py files. To retrain them, run a command like `python knn.py 1000`. The numerical argument is the number of positive and negative samples to use while training, and should be the same as the argument used for the preparedata.py command. 
