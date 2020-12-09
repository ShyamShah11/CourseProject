# ExpertSearch: Identifying Faculty Webpage URLs

## Proposal
The project proposal is in the file called [proposal.pdf](./proposal.pdf).

## Progress Report
The progress report is in the file called [progress_report.pdf](./progress_report.pdf)

## Implementation
I decided that I did not need to use the ExpertSearch code for this but I did use some of the ExperSearch data. I can isolate the task of classifying URLs from the rest of the functionality provided by ExpertSearch so this project will be me working on it seperately (for now).

Everything implementation related is in this [folder](./code). In the data [folder](./code/data), I have a file for positive training data and negative training data. The positive training data has examples of actual faculty URLs and is taken directly from [here](https://github.com/CS410Fall2020/ExpertSearch/blob/master/data/urls). The negative data has examples of non faculty URLs from university pages as well as all of the directory URLs themselves from the MP2.1 signup spreadsheet. The code for generating these is in [scraper.py](./code/scraper.py).

Note: the scraper uses selenium which requires chromedriver.exe to either be on your PATH, or in the same directory as scraper.py. 

For features, I used tokens from the URL (ie. everything seperated by a non alphabetic characters) first. After a few tests, I decided to use only the tokens that were also English words. [preparedata.py](./code/preparedata.py) converts the datasets into [feature vectors](./code/data/feature_vectors) which are used for the different algorithms, and it counts the [term frequency](./code/data/term_frequency) over all URLs. I have only uploaded feature vectors for a small subset of my data to avoid file size constraints.

The three classifiers I experimented with were [Naive-Bayes](./code/naivebayes.py), [maximum entropy](./code/maxentropy.py), and [k-nearest neighbors](./code/knn.py). 

I used [this paper](https://ingmarweber.de/wp-content/uploads/2013/07/A-Comprehensive-Study-of-Features-and-Algorithms-for-URL-Based-Topic-Classification.pdf) to help come up with some of the ideas used for this project.
