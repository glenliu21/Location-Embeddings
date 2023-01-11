# Location Embeddings
In this project, I trained a model to produce embeddings of zipcodes using the Skip-Gram Word2Vec model with user clickstreams as training data. This project was developed during my internship with [OJO Labs](https://ojo.com/), a real estate technology startup.

## Motivation
How can we derive a model for zipcodes such that they can be quantitatively analyzed, compared, and then passed into further machine learning models as a feature? This task is challenging because of how much information can be encoded into zipcodes. A non-trivial question is what exactly does it mean for two zipcodes to be similar? For instance, zipcodes could be similar because they have similar house prices despite the fact that they are not geographically adjacent. Zipcodes could also be similar for a number of other different factors, such as whether or not they share certain house amenities or whether or not they are located in the same school zone. 

## The Model
To handle this difficulty, I used a corpus of user clickstreams taken from [Movoto](https://www.movoto.com/), a home listing site, and fed it into [Gensim's Word2Vec model](https://radimrehurek.com/gensim/models/word2vec.html). This self-supervised learning approach essentially allowed customers to determine what made certain zipcodes similar. This is in contrast to me passing in a list of features that a model should train on, which would've been less comprehensive and less accurate with respect to our goal of providing similar home recommendations to a prospective homebuyer. 

To see the code for model training, please see the first couple of cells of the [zipcode-embeddings notebook](zipcode-embeddings.ipynb). See the [movoto_clickstream_processing notebook](movoto_clickstream_processing.ipynb) to examine how I parsed page hits into a corpus of user clickstreams using PySpark. 

## Evaluation
First, I wanted to see how well my zipcode embeddings could be used to predict certain indices, such as median listing home price. To do this, I trained a deep neural network which took in my embeddings as input and outputted a prediction of the target index for each embedding. I also made sure to tune the deep neural network's hyperparameters using Keras' CVTuner so that I had the most optimized neural network architecture. 

The second method of evaluating my zipcode embeddings was seeing how well they performed on a triplet loss test. In this test, the anchor input was the zipcode that a customer first browsed on, the positive input was the zipcode that the customer ended up transacting on, and the negative input was the zipcode that was geographically closest to the anchor. Then, I would calculate the positive similarity (ie the cosine similarity between the anchor and the positive) as well as the negative similarity then divide the latter by the former. The underlying assumption is that for each transaction, the zipcode that the user ended up transacting on should be more similar to the anchor than the zipcode geographically closest to the anchor. Thus, the goal for each test was to have an outputted value less than 1. 

To see the code for my tests, see the [zipcode-embeddings notebook](zipcode-embeddings.ipynb).

## Results
Out of all the tests, my zipcode embeddings performed best when they were used to predict median listing home prices in a zipcode. For this test, they outperformed baseline predictions by about 70% (ie when randomized n-dimensional embeddings were used as input to the deep neural network). Some outliers that drastically increased loss were zipcodes with very few transactions or with low-quality clickstreams (for instance, the user was clicking on zipcodes in the suburbs of the Midwest and in Manhattan). It's also important to note that zipcodes themselves are also a somewhat flawed and arbitrary way to group homes, and thus some zipcodes have very high variance when it comes to home prices and other features. 
