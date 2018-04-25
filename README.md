This is the main web page of our final project "Intelligent Yelp Recommendation System" for class CS525/DS595: Information Retrieval & Social Web at Worcestor Polytechnic Institute (WPI).

Our team consists of four members: Sarun Paisarnsrisomsuk, Tesia Shizume, Anthony Topper, and Fangling Zhang.

The goal of our project is to build a recommendation system to predict a rating that a user will give to a restaurant. We use dataset from Yelp Dataset Challenge (https://www.yelp.com/dataset/challenge). We applied several methods, some of which we have learned in class, to make the prediction.

The original dataset consists of 1,326,101 users, 174,567 business, and 5,261,669 reviews. Since our main focus for this project involves around suggestion of restaurants, we first reduce the dataset to have only business with "Restaurants" as one of their categories. We also filter out users who has less than 3 reviews. Then we randomly choose 5000 business. Our reduced dataset consists of 17,153 users, 4,733 business, and 90,251 reviews.

Our project is divided into four parts:
1) Applying K-mean Clustering Algorithm
2) Applying Collaborative Filtering Algorithm
3) Applying AutoEncoder, Restricted Boltzmann Machine (RBM), Latent Factor Model
4) Using other available attributes to make a prediction



Part 1: Applying K-mean Clustering Algorithm




Part 2: Applying Collaborative Filtering Algorithm




Part 3: Applying AutoEncoder, Restricted Boltzmann Machine (RBM), Latent Factor Model

run code 'ae.py', 'rbm.py' and 'lfm-tf.py'. 
This part needs you to install pytorch and tensorflow firstly.



Part 4: Using other available attributes to make a prediction
