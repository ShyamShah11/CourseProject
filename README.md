# ExpertSearch: Identifying Faculty Webpage URLs

## Proposal
The project proposal is in the file called [proposal.pdf](./proposal.pdf).

## Progress Report
The progress report is in the file called [progress_report.pdf](./progress_report.pdf)

## Demonstration
Check the README in the [code folder](./code) for instructions. 

## Implementation
I decided that I did not need to use the ExpertSearch code for this but I did use some of the ExperSearch data. I can isolate the task of classifying URLs from the rest of the functionality provided by ExpertSearch so this project will be me working on it seperately (for now).

Everything implementation related is in this [folder](./code).

## Preparing data
In the data [folder](./code/data), I have a file for positive training data and negative training data. The positive training data has examples of actual faculty URLs and is taken directly from [here](https://github.com/CS410Fall2020/ExpertSearch/blob/master/data/urls). The negative data has examples of non faculty URLs from university pages as well as all of the directory URLs themselves from the MP2.1 signup spreadsheet. The code for generating these is in [scraper.py](./code/scraper.py).

Note: the scraper uses selenium which requires chromedriver.exe to either be on your PATH, or in the same directory as scraper.py. 

## Data as feature vectors
For features, I used tokens from the URL (ie. everything seperated by a non alphabetic characters) first. After a few tests, I decided to use only the tokens that were also English words since the tokens that aren't English words are usually people's names or university name acronyms which I felt did not add enough value for the number of features they added. [preparedata.py](./code/preparedata.py) converts the datasets into [feature vectors](./code/data/feature_vectors) which are used for the different algorithms, and it counts the [term frequency](./code/data/term_frequency) over all URLs. I have only uploaded feature vectors for a small subset of my data to avoid file size constraints.

## Classifiers
The three classifiers I experimented with were [Naive-Bayes](./code/naivebayes.py), [maximum entropy](./code/maxentropy.py), and [k-nearest neighbors](./code/knn.py). I also tuned my models based on a small sample size of data (1000 total URLs) because of time and hardware constraints. 

### Naive Bayes
I experimented with 4 kinds of Naive Bayes classifiers: Gaussian, Bernoulli, complement, and multinomial. Over 400 test points, these were the results (accuracy is the number of correctly labelled URLs).

| Classifier    | Accuracy      |
| :-------------|:------------- |
| Gaussian      | 83%           |
| Bernoulli     | 87%           |
| Complement    | 79%           |
| Multinomial   | 49%           |

Based on this, I decided to go with a Bernoulli Naive Bayes classifier. One of the benefits of a Bayes classifier is that you get to use a prior. However since I had an even split of positive and negative samples in the data I used, the prior I chose to use was a uniform prior over the two labels. A possible improvement would be to modify the scraper to calculate a more realistic prior by calculating the amount of URLs on a university webpage that are faculty URLs. 

### K-nearest neighbors
For the k-nearest neighbors classifier, I experimented with using uniform weights and distance based weights. These were the results for uniform weights.

| k    | Accuracy      |
| :----|:------------- |
| 2    | 71%           |
| 3    | 84%           |
| 4    | 83%           |
| 5    | 84%           |
| 6    | 84%           |
| 7    | 83%           |
| 8    | 85%           |
| 9    | 84%           |
| 10   | 84%           |
| 11   | 85%           |
| 12   | 84%           |
| 13   | 83%           |
| 14   | 82%           |
| 15   | 82%           |
| 16   | 79%           |

And these were the results for distance based weights.

| k    | Accuracy      |
| :----|:------------- |
| 2    | 71%           |
| 3    | 84%           |
| 4    | 84%           |
| 5    | 85%           |
| 6    | 85%           |
| 7    | 84%           |
| 8    | 86%           |
| 9    | 86%           |
| 10   | 86%           |
| 11   | 88%           |
| 12   | 86%           |
| 13   | 86%           |
| 14   | 86%           |
| 15   | 85%           |
| 16   | 85%           |

Based on these results I went with k=11 and using distance based weights.

### Maximum entropy
For the maximum entropy classifier, I first had to make changes to how my data was being represented. The nltk [MaxEntClassifier](https://www.nltk.org/_modules/nltk/classify/maxent.html) requires a dictionary instead of an array to be trained over. So instead of using the same feature vectors, I converted them back to dictionaries of tokens. I experimented with the GIS and the IIS algorithms. With 100 iterations, the GIS algorithm classified 92% of the test points correctly, and the IIS algorithm had 91% accuracy. The accuracy for both algorithms went down when I tried again with 500 iterations so I stuck with the GIS algorithm and 100 iterations.

I used [this paper](https://ingmarweber.de/wp-content/uploads/2013/07/A-Comprehensive-Study-of-Features-and-Algorithms-for-URL-Based-Topic-Classification.pdf) to help come up with some of the ideas used for this project.
