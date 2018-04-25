import simplejson as json
from langdetect import detect

# Primary author: ttshiz

# make_categories()
# creates and writes to a file the ordered set of categories found in the business.json file, this can
# later be filtered to create a whitelist of categories, for filtering of the reviews
# @params - business_filename a yelp style business.json file containing the field categories
# @returns - the ordered set of categories for all the reviews in the dataset
def make_categories(business_filename):
    with open(whitelist_filename) as fp:
        business_categories = []
        #i= 0
        for lin in fp:
            data_received = json.loads(lin.rstrip())
            business_categories.extend(data_received["categories"])
            #i += 1
            #if ((i+1)%1000 == 0):
            #    print("Entry %d\n" % (i+1))
        category_set = set(business_categories)
        with open("categories.txt", 'w') as writefile:
            for item in sorted(category_set):
                writefile.write("%s\n" % item)
    return category_set

# make_business_id_list()
# creates and saves to a file a whitelist of business_ids with at least one category entry equal to
# "restaurant"; alternatively can use a whitelist of categories instead of the singleton, as noted in
# the comments
# @returns - the set of whitelisted business_ids
def make_business_id_list():
    # uncomment the following and enter whitelist_filename to use the whitelist
    #with open(whitelist_filename) as fp:
    #    category_list = []
    #    for ln in fp:
    #        category_list.append(ln[:-1])
    with open("business.json") as businesses:
        business_ids = []
        i = 0
        c = 0
        for lin in businesses:
            data_received = json.loads(lin.rstrip())
            categories = data_received["categories"]
            for cat in categories:
                # invert the commenting on next two lines to use whitelist if using whitelist
                #if cat in category_list:
                if cat  == "Restaurants":
                    business_ids.append(data_received["business_id"])
                    c += 1
                i += 1
                if ((i+1)%10000 == 0):
                    print("Entry %d\n" % (i+1))
        out_filename = "strict_business_ids.txt"
        with open(out_filename, 'w') as writefile:
            business_set = set(business_ids)
            for item in sorted(business_set):
                writefile.write("%s\n" % item)
        print("number of business ids: " + str(c))
    return business_set

# make_review_subset()
# creates a .json file for the subset of reviews allowed by a business_id whitelist file; has comments
# for print statements if a verbose version is desired
# @param reviews_filename - the yelp-style reviews.json or similarly formated file
# @param business_ids_file - the whitelist of business_ids
# @param extension_len - the length of the extension in the business_ids file, for consistent naming
# purposes (ex:"category_whitelist_v1.txt" has an extention length of 7, 4 for .txt and 3 for _v1
# @return c - the count of accepted reviews
# @return i - the count of processed reviews
def make_review_subset(reviews_filename, business_ids_file, extension_len):
    with open(business_ids_file, 'r') as ids:
        id_list = set()
        i = 0
        c = 0
        for ln in ids:
            id_list.add(ln[:-1])
        print("num ids", len(id_list))
    with open(reviews_filename, 'r') as reviews:
        outfilename = "strict_restaurant_reviews" + business_ids_file[(-1*extension_len):-3] + "json"
        with open(outfilename, 'w') as outfile:
            for lin in reviews:
                data_received = json.loads(lin.rstrip())
                if data_received["business_id"] in id_list:
                    outfile.write(lin)
                    c += 1
                    #if ((c+1)%10000 == 0):
                    #    print("Review %d\n" % (c+1))
                i += 1
                #if ((i+1)%100000 == 0):
                #    print("Entry %d\n" % (i+1))
    return c, i
           

# main()
# filters the Yelp dataset for restaurant reviews and writes these reviews as a new .json data file;
# intermediate stages provided for adjustment or other tuning
def main():
    # create categories file for further filtering
    categories = make_categories("business.json")

    # the below is an example of the make_business_id_list function call with whitelist enabled
    #businesses = make_business_id_list("category_whitelist_v1.txt", 7)

    # create the business_id_list for restaurants
    businesses = make_business_id_list()

    # create the review subset file
    reviews = make_review_subset("reviews.json", "strict_business_ids.txt", 4)
    
if __name__ == "__main__":
    main()
                        
