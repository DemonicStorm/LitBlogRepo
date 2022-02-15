import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()

#nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)


'''Die txt-Dateien der Blogeinträge über manuell erstellte übersichts.csv (einzeln) anwählen, welche besonders 
interessant für nähere Analyse sind und den Pfad mit ID, die Sprache pro Satz und die Tokenanzahl ausgeben lassen'''


def main():
    pathList = []  # zum befüllen der Pfade zu den txt, die analysiert werden sollen
    with open("/home/mherbert/Desktop/neu_test_meta/5949_x.csv", encoding="utf-8") as file: #der Pfad muss für jeden Blog aktualisiert werden
        for i in file:
            if i.split(";")[-1] != "x":
                '''Der Pfad muss für jeden Blog aktualisiert werden und bis vor das Blogverzeichnis gehen und darf nicht
                 mit / enden, weil das die Joinfunktion automatisch dazwischensetzt. Nach exrtraction 5/ muss die 
                 BlogID, welche im metapath schon angewählt wird stehen. Über i.split wird jeweils die BeitragsID angehängt
                  und anschließend die txt-Datei.'''
                pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/5949", i.split(";")[0],"extracted.txt"]))
    #print(pathList)
    resultList = []
    for path in pathList:
        with open(path, encoding="utf-8") as open_file:
            t_content = open_file.read()
        #print(t_content)
        j = 0
        lang = nlp(t_content)
        for i, sent in enumerate(lang.sents): #langdetect über jeden Satz iterieren 
            lang_2 = (sent._.language)
            tokenanzahl = len(sent) #Tokenanzahl pro Satz für die relative Anzahl an verschiedenen Sprachen innerhalb eines Blogs
            j = j+1 #für jeden satz eine eigene ID erstellen 
            path_neu = []
            path_neu.append(path + "/" + str(j)) #ID an Path anhängen
            lang_3 = (path_neu, lang_2, tokenanzahl)
            resultList.append(lang_3)
    print(resultList)


main() #main-Funktion ausführen

