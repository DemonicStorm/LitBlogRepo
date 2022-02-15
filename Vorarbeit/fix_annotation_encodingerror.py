"""
Liest unannotierte Meta-CSV und Annotierte in DataFrame ein, um die 
encoding-Fehler aus den Annotierten Dateien zu umgehen, indem die Annotations-
spalte des Annotierten Dataframes in den unannotierten Dataframe eingefügt wird.
"""
import pandas as pd
import glob

a_paths = glob.glob("/home/dsturm/Desktop/litblogs/Austauschordner/bereinigte Metas/**.csv")

headline = ["Page","txtlen","url","sitename", "date", "categories", "autor", "titel", "hostname","manAnno","scrAnno"]

for path in a_paths:
    try:
        dir_nr = path.split("/")[-1].split("_")[0]
        ann = pd.read_csv(path, sep=";", engine="python", names= headline)
        un = pd.read_csv("/home/dsturm/Desktop/litblogs/Austauschordner/Metas/" + dir_nr + ".csv", sep=";", engine="python",names=headline)

        un["manAnno"] = ann["manAnno"]

        un.to_csv("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/clean/"+ dir_nr + "_X.csv",header=True, index =False, encoding="utf-8", sep=";")
        print(dir_nr, " completed")
    except:
        print("Exception: ", dir_nr)
