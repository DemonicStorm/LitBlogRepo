import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()

#nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)



'''die txt der Blogeinträge anwählen (über manuell erstellte übersichts.csv), welche besonders interessant für nähere Analyse sind 
und Sprache pro Dokument und pro Satz ausgeben lassen'''


# metapath ist dazu da, die bereinigte csv anzuwählen, und die  welchen man durch Skript laufen lassen will
def main():
 # zum befüllen der txtpfade, die angewählt werden sollen
    #blognr = mp.split("/")[-1].split("_")[0] #wählt die Blognummer an, wenn man das Skript durch den gesamten extractions5 ordner laufen lässt
    path = "/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/2759/24/extracted.txt"
    # print(pathList)
    resultList = []
    with open(path, encoding="utf-8") as open_file:
        t_content = open_file.read()
        #print(t_content)
    lang = nlp(t_content)
    for i, sent in enumerate(lang.sents): #langdetect über jeden Satz iterieren 
        lang_2 = (sent, sent._.language)
        #print(sent._.language)
        #lang_3 = (path, lang_2)
        resultList.append(lang_2)
    print(resultList)
    #return resultList


a = "/home/mherbert/Desktop/neu_test_meta/5886_x.csv"

main()