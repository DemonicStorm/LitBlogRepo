import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

'''Die txt-Dateien der Blogeinträge über manuell erstellte übersichts.csv (einzeln) anwählen und die Sprache analysieren. 
Anschließend Blogeintragspfad und Sprache zusammen ausgeben lassen '''


# metapath ist dazu da, die bereinigte csv anzuwählen, und die  welchen man durch Skript laufen lassen will
def main(metapath):
    mp = metapath
    pathList = []  # zum befüllen der txtpfade, die angewählt werden sollen
    with open(mp) as file:   
        for i in file:
            if i.split(";")[-1] != "x":
                '''Der Pfad muss für jeden Blog aktualisiert werden und bis vor das Blogverzeichnis gehen und darf nicht
                 mit / enden, weil das die Joinfunktion automatisch dazwischensetzt. Nach exrtraction 5/ muss die 
                 BlogID, welche im metapath schon angewählt wird stehen. Über i.split wird jeweils die BeitragsID angehängt
                  und anschließend die txt-Datei.'''
                pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/5935", i.split(";")[0],"extracted.txt"]))
    resultList = []
    for path in pathList:
        with open(path, encoding="utf-8") as open_file:
            t_content = open_file.read()
        lang = nlp(t_content)
        lang_2 = lang._.language #Sprache ermitteln über diesen Befehl
        lang_3 = (path, lang_2) #Pfad und Sprachergebnis in einer Variablen abspeichern
        resultList.append(lang_3) #Veriable an Liste anghängen
        #print(lang_2)
    print(resultList)
    return resultList


a = "/home/mherbert/Desktop/neu_test_meta/5935_x.csv" #Pfad muss für jeden Blog aktualisiert werden

main(a)

#anschließend Ergebnisse in txt-Datei abspeichern (manuell)
