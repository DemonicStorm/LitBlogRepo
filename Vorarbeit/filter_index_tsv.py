import shutil
import os
import json
import glob
from nltk.tokenize import wordpunct_tokenize as tok
from itertools import combinations
"""
Line-Objekt für einzelne Zeilen in Index.tsv
"""
class Line(object):

    def __init__(self, string):
        self.string = string
        self.t_hash = string.split()[3]
        self.url = string.split()[0]
        self.oldpath = string.split()[1]
        self.hash1 = string.split()[2]

def filter(quelldatei, zieldatei):
    """
    Einlesen der Daten und prüfen ob Objekte mit dem text-hash in der Liste
    enthalten sind, if not wird das Objekt der Liste hinzugefügt.
    Dann werden alle Lines der Liste in Ausgabefile geschrieben.
    """
    with open(quelldatei, "r", encoding="utf-8") as f:
        liste = []
        for line in f:
            obj = Line(line)
            if obj.t_hash in [i.t_hash for i in liste]:
                 pass
            else:
                liste.append(obj)
    # Ausgabe der Strings der Objekte
    out = open(zieldatei, "w", encoding="utf-8")
    for i in liste:
        out.write(i.string)
    out.close()

