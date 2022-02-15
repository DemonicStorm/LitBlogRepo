import csv
import pandas as pd

# Vergleicht die keywordergebnisse aller Blogs mit den Ergebnissen bei Einzelblogs
def vgl(corpusfile,blogfile):
    """

    :param corpusfile: str Dateipfad/-name keywords aller Blogs
    :param blogfile: str Dateipfad/-name keywords eines Blogs
    :return: listen: gemeinsamer keywords, keywords in Korpus und nicht in Blog, keywords nicht in Korpus und in Blog
    """
    from ast import literal_eval
    blog = pd.read_csv(blogfile,sep=",", index_col=False,converters={'keywords':literal_eval})
    blognr = int(blogfile.split("\\")[-1].split(".")[0].split("_")[1])
    corp = pd.read_csv(corpusfile,sep=",",index_col=False,converters={'keywords':literal_eval})
    corp_part = corp[corp["blog"] == blognr]
    bloglist = [x for x in blog["keywords"]]
    corplist = [x for x in corp_part["keywords"]]
    common = []
    c_not_b = []
    b_not_c = []
    for indx in range(len(bloglist)):
        listB = bloglist[indx]
        listC = corplist[indx]
        common.append([word for word in listB if word in listC])
        c_not_b.append([word for word in listC if word not in listB])
        b_not_c.append([word for word in listB if word not in listC])

    return common, c_not_b, b_not_c


common, corpus, blog = vgl("keywords_full.csv","keywords_3606.csv")
head = []
i = 0
while i < len(common):
    head.append([common[i], corpus[i], blog[i]])
    i += 1
df = pd.DataFrame(head, columns= ["common","corpus","blog"])
# common len column to dataframe
df["com_count"] = df.apply(lambda row : len(row[0]), axis=1)
import statistics as st
print("mean(common): ", st.mean(df["com_count"]))
# Frequenzen der Werte
df.com_count.value_counts()
pages = pd.read_csv("keywords_3606.csv")["dir"]
out = pages.to_frame().merge(df,left_index=True, right_index = True)
out.to_csv("VGL_3606.csv",index=False)