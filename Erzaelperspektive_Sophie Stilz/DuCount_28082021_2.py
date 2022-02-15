import csv
import os
import pickle
import nltk
from glob import glob


paths = glob("/home/sstilz/Desktop/clean/*_X.csv")
for i, csv_path in enumerate(paths):
    print(f"{i+1}/{len(paths)}")

    site_name = os.path.basename(csv_path).split("_")[0]
    pathList = []
    with open(csv_path, newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        for row in csvreader:
            if row[0].startswith("Page"):
                continue
            if row[-2] != "True":
                path = os.path.join("/home/sstilz/Desktop/litblogs/Kursmaterial/extraction5/", site_name, row[0] ,"extracted.txt")
                pathList.append(path)

        resultList = []
        search_list = ["du", "Du", "DU", "deiner", "Deiner", "DEINER", "dich", "Dich", "DICH", "dir", "Dir", "DIR", "ihr", "Ihr", "IHR", "euer", "Euer", "EUER", "euch", "Euch", "EUCH"]
        for path in pathList: 
            if not os.path.exists(path): 
                continue
            with open(path, encoding="utf-8") as open_file:
                t_content = open_file.read()
                tokens = nltk.wordpunct_tokenize(t_content)
            count = 0
            for token in tokens:
                if token.lower() in search_list:
                    count += 1
            resultList.append((path, count))

        # print(resultList)


    with open(site_name + "_du-count" + ".pkl", "wb") as outfile:
        pickle.dump(resultList, outfile)
        
