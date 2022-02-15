## Extracting Important Keywords from Text with TF-IDF and Python's Scikit-Learn
import pandas as pd
import re
import glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import csv

def build_corpus(csvfile):
    datapath = "/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5"
    file = open(csvfile,"r",encoding="UTF-8")
    reader = csv.reader(file,delimiter=";",quoting=csv.QUOTE_NONNUMERIC)
    paths = []
    for line in reader:
        if line[1] == "page" or len(line) == 0:
            pass
        else:
            path = "/".join([datapath,line[0],line[1],"extracted.txt"])
            paths.append(path)
    corpus = []
    for path in paths:
        with open(path,"r",encoding="UTF-8") as content:
            corpus.append((content.read(),path.split("/")[-2],path.split("/")[-3]))
    return corpus


def get_corpus_file(csvfile):
    fileID = csvfile.split("/")[-1].split("_")[0]
    datadir = "/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5"
    file = open(csvfile,"r",encoding="UTF-8")
    reader = csv.reader(file,delimiter=";",quoting=csv.QUOTE_NONE)
    paths = []
    for line in reader:
        if line[0] == "Page" or len(line) == 0:
            pass
        elif line[9] == "False":
            path = "/".join([datadir,fileID,line[0],"extracted.txt"])
            paths.append(path)
        else:
            pass
    corpus = []
    for path in paths:
        with open(path,"r",encoding="UTF-8") as content:
            corpus.append((content.read(),path.split("/")[-2],path.split("/")[-3]))
    return corpus


def get_corpus(directory):
    path = "/".join([directory,"*","extracted.txt"])
    paths = glob.glob(path)
    texts = []
    for i in paths:
        with open(i, encoding="utf-8") as f:
            texts.append((f.read(),i.split("/")[-2],i.split("/")[-3]))
    return texts


def pre_process(text):
    # lowercase
    text = text.lower()
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    return text

def get_stop_words(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = []
        for line in f.read():
            if line.startswith(";") is False:
                stopwords.append(line)
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]
    return results


# Daten
# über einzelnen Blog
corpus = get_corpus_file("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/clean/3218_X.csv")
# über alle Blogs
#corpus = build_corpus("metaintegration_test_2.csv")
df = pd.DataFrame(corpus, columns=["text","dir","blog"])
df["text"] = df["text"].apply(lambda x: pre_process(x))

#idf
docs = df["text"].tolist()
stopwords = get_stop_words("german_en_stopwords.txt")
cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
word_count_vector = cv.fit_transform(docs)

#transform idf to tfidf
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
# you only needs to do this once
feature_names = cv.get_feature_names()
results = []
for doc in docs:
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
    results.append(list(keywords.keys()))
df["keywords"] = results
print(df)
df.to_csv("keywords_3218.csv",index_col=False, quoting= csv.QUOTE_NONE)
