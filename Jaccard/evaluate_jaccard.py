import pandas as pd
import numpy as np
import glob
def df_anno_bool(csv_path,header= False):
    # Lädt CSV als Dataframe ein und ändert Annotation in True/False
    
    if header: 
        df = pd.read_csv(csv_path, sep=";", header=0, engine="python")
    else:
        headline = ["Page","txtlen","url","sitename", "date", "categories", "autor", "titel", "hostname","manAnno","scrAnno"]
        df = pd.read_csv(csv_path, sep=";", names=headline, engine="python")
    #df["manAnno"] = df["manAnno"].fillna(False)
    #df["scrAnno"] = df["scrAnno"].fillna(False)
    try:
        df.loc[df.manAnno == "x", "manAnno"] = True
    except:
        print("Exception, probably already Boolean")
    try:
        df.loc[df.scrAnno == "x", "scrAnno"] = True
    except:
        print("Exception, probably already Boolean")
    #print(df)
    df.to_csv(csv_path, header=True, index =False, encoding="utf-8", sep=";")
    
    
def check_ann(csv_path):
    df = pd.read_csv(csv_path, sep=";", header=0, engine="python")
    #print(df)
    conditions = [
            (df["manAnno"] == df["scrAnno"]) & df["manAnno"],
            (df["manAnno"] == df["scrAnno"]) & (df["manAnno"] == False),
            (df["manAnno"] == True) & (df["scrAnno"] == False),
            (df["manAnno"] == False) & (df["scrAnno"] == True)]
    choices = ["TP","TN","FN","FP"]
    df["eval"] = np.select(conditions,choices)
    #print(df)
    tp, tn, fn, fp = (df["eval"].values == "TP").sum(),(df["eval"].values == "TN").sum(), (df["eval"].values == "FN").sum(), (df["eval"].values == "FP").sum()
    print("TP: ", tp)
    print("TN: ", tn)
    print("FN: ", fn)
    print("FP: ", fp)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f_score = ((2*precision * recall)/(precision + recall))
    print("Precision: ", precision)
    print("Recall: ",recall)
    print("F-Score: ",f_score)
    #data_dict= {"param":,"blog":;"TP":,"TN":,"FN":,"FP":,"Precision":,"Recall":,"F-Score":}

    #df.to_csv(csv_path, header=True, index =False, encoding="utf-8", sep=";")
# gibt anhand metas die textpfade
def get_corpus(csv_meta):
    blog_nr = csv_meta.split("/")[-1].split("_")[0]
    txt_paths = []
    with open(csv_meta) as file:
        for i in file:
            splitted = i.split(";")
            if splitted[-1] == "False":
                txt_paths.append("/".join(["/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5",blog_nr,splitted[0],"extracted.txt"]))
    return txt_paths
 
paths = glob.glob("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/**.csv")
# in einer schleife funktionierte es nicht, daher erst anno_bool eingekommentiert und check_ann auskommentiert, dann andersrum
# Konsolenoutput rauskopiert und in Notepad++ umgeformt für Scriptlesbarkeit beim automatischen plotten.
for path in paths:
    print(path)
    #df_anno_bool(path)
    check_ann(path)
#check_ann("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5846_x.csv")