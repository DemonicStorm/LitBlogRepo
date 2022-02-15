import json
import matplotlib.pyplot as plt
import numpy as np
datapath = "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/Jaccard/Ergebnisse_Jaccard.txt"

with open(datapath, "r", encoding="utf-8") as file:
    dictList = {}
    for i in file:
        if i == "-":
            pass
        if len(i)>= 3 and len(i) <= 17:
            d = {str(i[:-1]): {}}
            dictList.update(d)
        elif len(i) > 15:
            try:
                splid = i.split("\t")
                key = list(dictList.keys())[-1]
                a = {splid[0].split("_")[0] : { splid[1].split(":")[0]: int(splid[1].split(":")[1]),
                                           splid[2].split(":")[0]: int(splid[2].split(":")[1]),
                                           splid[3].split(":")[0]: int(splid[3].split(":")[1]),
                                           splid[4].split(":")[0]: int(splid[4].split(":")[1]),
                                           splid[5].split(":")[0]: float(splid[5].split(":")[1]),
                                           splid[6].split(":")[0]: float(splid[6].split(":")[1]),
                                           "F_Score" : float(splid[7].split(":")[1])}}
                dictList[key].update(a)
            except:
                print(i)

import pandas as pd
print(len(dictList))


for inst in dictList:
    df = pd.DataFrame(dictList[inst]).swapaxes("columns","index")
    df_p = df.drop(columns=["FP", "TP", "TN", "FN"])
    df_p.plot(subplots=True, kind='bar', grid=True, ylim=(0, 1), title=" ".join(["Jaccard",inst]), legend=False)
    plt.savefig("/".join(["/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/Jaccard/plots",(inst + ".jpg")]))

