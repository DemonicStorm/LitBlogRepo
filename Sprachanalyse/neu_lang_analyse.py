from textblob import TextBlob
#from glob import glob
#from csv import reader
import time

'''die Blogeinträge anwählen als Sammlung an txt-Dateien (pro Blog)
die txts anwählen und mit textblob Sprache analysieren
anschließend Blogeintragspfad und Sprache zusammen ausgeben lassen '''



# metapath ist dazu da, die bereinigte csv anzuwählen, und die  welchen man durch Skript laufen lassen will
def main(metapath):
    mp = metapath
    pathList = [] #zum befüllen der txtpfade, die angewählt werden sollen
    with open(mp) as file:
        for i in file:
            #print(i)
            #print(i.split(";")[-2)
            if i.split(";")[-2] == "False":
                '''pfad muss für jeden Blog aktualisiert werden und bis vor das blogverzeichnis gehen und darf nicht mit / enden,
                weil das die joinfunktion automatisch dazwischensetzt.'''
                pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/2695", i.split(";")[0], "extracted.txt"]))
    #print(pathList)
    resultList = []
    for path in pathList:
        with open(path, encoding="utf-8") as open_file:
            t_content = open_file.read()
        lang = TextBlob(t_content)
        lang_2 = (path, lang.detect_language())
        time.sleep(10) #pause in sek, um request error evtl zu umgehen 
        resultList.append(lang_2)
    print(resultList)
    return resultList

#blogPath = "./2759"
metapath = "/home/mherbert/Desktop/test_meta/2695_X.csv"
result = main(metapath)

#print(result)

#speichern in txt (vorläufig)
open("lang.txt", "w", encoding="utf-8").close()
def save(result):
    outfile = open("lang.txt", "a", encoding="utf-8")
    outfile.write(result)
    outfile.close()
    
save(result)