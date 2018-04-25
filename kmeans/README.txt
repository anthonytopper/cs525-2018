--CS525 / DS595 Information Retrieval and the Social Web
-Group Project 2018

-Subsection leader: Tes Shizume

-Overview of k-means section:

The kmeans portion of this project was meant to be used as preprocessing for the later stages of the
project.

The working code of this portion of the project can be found in two files:
make_business_list.py
do_tf_idf.py

make_business_list.py contains preprocessing functions to filter the raw reviews file for the desired
subset for the project.

do_tf_idf.py contains the functions for tf-idf vectorization of the review text and kmeans clustering

This code uses the following libraries:
sklearn
langdetect
pickle
time
simplejson
shutil
csv
multiprocessing

It is possible to disable the code that uses langdetect for better time-performance.

pickle files are provided for the users convenience where time-intensive computation was used
(training vectorizer, kmeans, etc.), but should be used only if permitted by sys-admin.

The primary function developed for use in the later stages of the project is predict(min_df, k, review)
in the do_tf_idf.py file and this was intended to be the interface with the rest of the project.
