from textblob import TextBlob
from glob import glob
from csv import reader

'''die Blogeinträge anwählen als Sammlung an txt-Dateien (pro Blog)
die txts anwählen und mit textblob Sprache analysieren
anschließend Blogeintragspfad und Sprache zusammen ausgeben lassen '''


def meta(metaPath):  # herausfiltern, welche txt.-Dateien laut der bereinigten Meta-Dateien angesteuert werden sollen
    cmp = metaPath + "/*.csv"  # cmp steht für cleaned metapath
    mp = glob(cmp)
    # print(mp)
    blogEintrNr = []

    for csv in mp:
        with open(csv, newline='') as open_meta:
            m_content = reader(open_meta, delimiter=';') #csv so anwählen, dass man auf die einzelnen Zellen zugreifen kann
            #print(m_content)
            for row in m_content:
                #print(row)
                if row[9] != 'x': #filtern, dass kein x in Zeile vorhanden ist und dies Nummern (Spalte B) in Liste blogEintrNr abspeichern
                    blogEintrNr.append(row[1])
    #print(blogEintrNr)
    return blogEintrNr

#todo: blogEintrNr-Liste mit main verknüpfen, sodass nur diese angewählt werden


# blogPath ist dazu da, den Blog anzuwählen, welchen man durch Skript laufen lassen will
def main(blogPath):
    tp = blogPath + "/**/extracted.txt"  # tp steht für text pfad
    p = glob(tp)
    # print(p)
    pathList = []
    for path in sorted(p):
        with open(path, encoding="utf-8") as open_file:
            t_content = open_file.read()
        lang = TextBlob(t_content)
        lang_2 = (path, lang.detect_language())
        pathList.append(lang_2)
    #print(pathList)
    # todo: abspeichern in ein anderes doc bzw. in meta liste übertragen?
    return pathList

# todo: Liste mit gespeicherten Path bzw. Liste aus def meta vergleichen und doppelte entfernen

blogPath = "./2759"
textList = main(blogPath)
# metaPath = "/home/mherbert/Desktop/litblogs/Austauschordner/bereinigte Metas/"
metaPath = "./meta"
blogList = meta(metaPath)

print(textList)
print(blogList)