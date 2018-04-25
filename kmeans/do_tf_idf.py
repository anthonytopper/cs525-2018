
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
from langdetect import detect
import pickle
import time
import simplejson as json
import shutil
import csv
from multiprocessing import Pool

pfn = "strict_exploration_nonmini.pickle"

# memodisk(flnm):
# this is a helper for memoization of the stages of clustering using pickle to minimize duplicated
# effort writes the function results to a pickle file with the provided name
# @param flnm - the name for the pickle file, defaults to the empty string
def memodisk(flnm=""):
    def dec(fn):
        fn.m = None
        def helper():
            if fn.m is not None:
                print("Got "+flnm+" from RAM cache!")
                return fn.m
            else:
                start = time.time()
                try:
                    with open(flnm+".pickle", "rb") as p:
                        print("Loading "+flnm+" from disk.")
                        fn.m = pickle.load(p)
                        end = time.time()
                        print("Got "+flnm+" from disk cache in "+str(end-start)+" seconds!")
                except:
                    print("Calculating "+flnm+" ...")
                    fn.m = fn()
                    end = time.time()
                    print("calculated "+flnm+" in "+str(end-start)+" seconds, saving it to disk ...")
                    with open(flnm+".pickle", "wb") as p:
                        pickle.dump(fn.m, p)
                    end = time.time()
                    print(flnm+" memoized in "+str(end-start)+" total seconds!")
                return fn.m
        return helper
    return dec

# data_lang_tuple(l):
# helper function for load_biz_rev_text(); performs optional language tagging of reviews creates a
# mini-dictionary with relevant parts, seperate function to facilitate multiple-workers if needed
# @params l - a json entry from a Yelp style json reviews file
# @return a dictionary
def data_lang_tuple(l):
    j = json.loads(l)
    try:
        # uncomment the next line to enable language filtering (this is VERY SLOW!)
        #leng = detect(j["text"])
        j["leng"] = "en"
    except:
        leng["leng"] = ""
    return dict([(k, v) for k, v in j.items() if k in ["business_id", "text", "user_id", "stars", "leng"]])

# load_biz_rev_text():
# creates a dictionary mapping business_id to values of interest for further processing
# @return -  a list of dictionaries where each dictionary has the information for a given business
@memodisk(flnm="strict_resturant_reviews")
def load_biz_rev_text():
    biz_review = {}
    for rev in map(data_lang_tuple, open("strict_restaurant_reviews.json")):
        biz = rev["business_id"]
        upBiz = biz_review.get(biz, {"biz_id": biz, "text":[], "stars":[], "users":[]})
        upBiz["text"].insert(0, rev["text"])
        upBiz["stars"].insert(0, rev["stars"])
        upBiz["users"].insert(0, rev["user_id"])
        biz_review[biz] = upBiz
    return list(biz_review.values())

# build_vectorizer():
# instantiates and trains a TfidfVectorizer on the dataset, concatenating by business for
# business-based recommenders (modifiable to concatenate by user for user-based analysis or other
# adjustments)
# @return - the trained vectorizer
@memodisk(flnm="strict_sparse_vectorizer_max0.625_min0.5")
def build_vectorizer():
    vectorizer = TfidfVectorizer(max_df=0.625, min_df=0.5)
    return vectorizer.fit(["".join(biz["text"]) for biz in load_biz_rev_text()])

# get_vectorizer():
# fetches the TfidfVectorizer from a pickle file, min_df was used to distinguish vectorizers since in
# the tunning stages it had a large impact on the size of the vector space
# @param min_df - the min_df used for training the vectorizer desired
# @return the trained TfidfVectorizer distinguished by min_df
def get_vectorizer(min_df):
    with open("strict_sparse_vectorizer_max0.99_min%s.pickle"%(str(min_df)), "rb") as p:
        vectorizer = pickle.load(p)
    return vectorizer

# calc_word_matrix():
# calculates the Tfidf vectors for the businesses
# @return - the Tfidf matrix for the businesses (or if adapted reviews or users)
@memodisk(flnm="strict_sparse_wordvec_max0.625_min0.5")
def calc_word_matrix():
    vectorizer = build_vectorizer()
    return vectorizer.transform(["".join(biz["text"]) for biz in load_biz_rev_text()])

# depreciated from raw review clustering attempt
# does a basic kmeans clustering on the dataset and returns the clustering
@memodisk(flnm="fullbatchkmeans")
def do_kmeans():
    km = KMeans(n_clusters=16, n_init=10, tol=0.01)
    clusters = km.fit(calc_word_matrix())
    return clusters

# depreciated from raw review clustering attempt, not used in business-based or user-based clustering
# calculates the number of times a business is in a cluster
@memodisk(flnm="fullbatch_cluster_members")
def find_top_10_cluster_members():
    clusters = do_kmeans()
    #vectorizer = build_vectorizer()
    
    cluster_associations = dict([(c, dict()) for c in range(len(clusters.cluster_centers_))])
    for (business, cluster) in zip([biz for (biz, txt) in load_rev_text()], clusters.labels_):
        cluster_associations[cluster][business] = cluster_associations[cluster].get(business, 0) + 1

    return cluster_associations

# run_km(min_df, k):
# attempts to load and return a cached trained kmeans clusterer for the given min_df and k values,
# if not available trains a kmeans clusterer for those parameters and returns the clusterer
# @param min_df - the min_df used to create the review tf-idf matrix, used as an distinguisher
# @param k - the number of clusters to use in clustering
# @return - a kmeans clusterer trained for k clusters, on review vectors transformed to tf-idf
# using min_df
def run_km(min_df, k):
    kmflnm = "strict_kmeans_min_df%s_k%d.pickle"%(str(min_df), k)
    
    try:
        with open(kmflnm, "rb") as p:
            km = pickle.load(p)
    except:
        print("Calculating min_df="+str(min_df)+", k="+str(k))
        pflnm = "strict_sparse_wordvec_max0.99_min"+str(min_df)+".pickle"
        with open(pflnm, "rb") as p:
            sm = pickle.load(p)
        print("Loaded cached min_df="+str(min_df))
        start = time.time()
        km = KMeans(n_clusters=k, n_jobs=-3, tol=0.01, precompute_distances=True, verbose=1)
        km.fit(sm)
        end = time.time()
    
        with open(kmflnm, "wb") as p:
            pickle.dump(km, p)
    
        print("With min_df="+str(min_df)+" and k="+str(k)+" the inertia was "+str(km.inertia_)+" in "+str(end-start)+" seconds.")

    return km

# predict(min_df, k, review):
# clusters text using a TfidfVectorizer trained with min_df and a Kmeans clusterer trained on data
# vectorized with that min_df for k clusters
# @param min_df - the minimum df percentage [0,1] accepted for words to be included in the TfidfVector
# @param k - the integer number of clusters
# @param review - a string of text to be clustered
def predict(min_df, k, review):
    km = run_km(min_df, k)
    vectorizer = get_vectorizer(min_df)
    p = km.predict(vectorizer.transform([review]))
    return p[0]

# test_km(a):
# helper function for explore_kmeans, runs one kmeans clustering based on parameters in a and wraps it
# in informative progress print statements
# @param a -  a tuple containing min_df, k, and sm; min_df a tunning parameter used in the
# TfidfVectorizer, k the desired number of clusters, and sm the data to be fit
# @returns - a tuple of the min_df value, the k value, and the inertia value found from the clustering
def test_km(a):
    min_df, k, sm = a
    print("Calculating min_df="+str(min_df)+", k="+str(k))
    start = time.time()
    km = KMeans(n_clusters=k, n_init=1, tol=0.01)
    km.fit(sm)
    end = time.time()
    print("With min_df="+str(min_df)+" and k="+str(k)+" the inertia was "+str(km.inertia_)+" in "+str(end-start)+" seconds.")
    return (min_df, k, km.inertia_)

# explore_kmeans()
# a multi-worker function to quickly explore the effect that varying k and min_df have on the
# performance of the kmeans clustering
def explore_kmeans():
    vectorizer = {}
    sm = {}
    dfs = [0.5, 0.25, 0.125, 0.0625] # , 0.03125, 0.015625, 0.01]
    ks = range(2, 1001, 2)

    try:
        with open(pfn, "rb") as p:
            data = pickle.load(p)
    except:
        data = {}
    
    start = time.time()
    for min_df in dfs:
        pflnm = "strict_sparse_wordvec_max0.99_min"+str(min_df)+".pickle"
        try:
            with open(pflnm, "rb") as p:
                sm[min_df] = pickle.load(p)
            print("Loaded cached min_df="+str(min_df))
        except:
            vectorizer[min_df] = TfidfVectorizer(max_df=0.99, min_df=min_df)
            sm[min_df] = vectorizer[min_df].fit_transform([txt for (biz, txt) in load_rev_text()])
            with open(pflnm, "wb") as p:
                pickle.dump(sm[min_df], p)
            print("Vectorized min_df="+str(min_df))
    end = time.time()
    print("Prepared vectorizers and sms in "+str(end-start)+" seconds")

    fps = [(min_df, k) for k in ks[:25] for min_df in dfs[:2]]
    sps = [(min_df, k) for k in ks for min_df in dfs if (min_df, k) not in fps]
    ps = fps+sps

    with Pool(8) as pool:
        for (min_df_, k_, iner) in pool.imap_unordered(test_km, [(p[0], p[1], sm[p[0]]) for p in ps if p not in data]):
            data[(min_df_, k_)] = iner
            # Backup last pickle file before writing new data
            try:
                shutil.move(pfn, "strict_exploration_backup.pickle")
            except:
                pass
            with open(pfn, "wb") as p:
                pickle.dump(data, p)

    print("Done!")

# biz_clusters(min_df, k):
# writes the association of business_ids to cluster number to a csv file for further processing
# @param min_df - the min_df used in the vectorization prior to the kmeans clustering for the desired
# clusterer
# @param k - the number of clusters desired
def biz_clusters(min_df, k):
    try:
        with open("strict_kmeans_min_df%s_k%d.pickle"%(str(min_df), k), "rb") as p:
            km = pickle.load(p)
    except:
        km = run_km(min_df, k)

    with open("k%d_mindf%s_clustering.csv"%(k, str(min_df)), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["business_id", "cluster"])
        for (cluster, biz) in zip(km.labels_, load_biz_rev_text()):
            csvwriter.writerow([biz["biz_id"], cluster])

# gen_csv():
# writes the inertia values found in explore_kmeans to a csv file for later data visualization
def gen_csv():
    with open(pfn, "rb") as p:
        data = pickle.load(p)
    dfs = sorted(list(set([df for df, k in data.keys()])))
    ks = sorted(list(set([k for df, k in data.keys()])))
    with open("inertia_exploration.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["k"] + ["min_df = "+str(df) for df in dfs])
        for k in ks:
            csvwriter.writerow([k] + [data.get((df, k), "") for df in dfs])
            
# used to enable running functions in commandline with optimized parameters
if __name__ == "__main__":
    explore_kmeans()
