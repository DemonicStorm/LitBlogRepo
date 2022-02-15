import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()

#nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

'''dinge ausprobieren'''
#text = "das hier dürfte deutsch sein."
#doc = nlp(text)
#print(doc._.language)



'''die Blogeinträge anwählen als Sammlung an txt-Dateien (pro Blog)
die txts anwählen und mit textblob Sprache analysieren
anschließend Blogeintragspfad und Sprache zusammen ausgeben lassen '''


# metapath ist dazu da, die bereinigte csv anzuwählen, und die  welchen man durch Skript laufen lassen will
def main(metapath):
    mp = metapath
    pathList = []  # zum befüllen der txtpfade, die angewählt werden sollen
    #blognr = mp.split("/")[-1].split("_")[0] #wählt die Blognummer an, wenn man das Skript durch den gesamten extractions5 ordner laufen lässt
    with open(mp) as file:   
        for i in file:
            # print(i)
            # print(i.split(";")[-2)
            if i.split(";")[-1] != "x":
                '''pfad muss für jeden Blog aktualisiert werden und bis vor das blogverzeichnis gehen und darf nicht mit / enden,
                weil das die joinfunktion automatisch dazwischensetzt. nach pfad steht blognr um durchs ganze Skript laufen zu lassen, ansonsten weglassen'''
                pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/5935", i.split(";")[0],"extracted.txt"]))
    # print(pathList)
    resultList = []
    for path in pathList:
        with open(path, encoding="utf-8") as open_file:
            t_content = open_file.read()
        #print(t_content)
        lang = nlp(t_content)
        lang_2 = lang._.language
        #path2 = path.split("/")[7]
        lang_3 = (path, lang_2)
        #time.sleep(10)  # pause in sek, um request error evtl zu umgehen
        resultList.append(lang_3)
    #print(resultList)
        print(lang_2)
    return resultList


a = "/home/mherbert/Desktop/neu_test_meta/5935_x.csv"

'''for i in a:
    main(i)''' # das anwenden, wenn alles eingelesen werden soll (mit glob vor dem metapfad) ansonsten 

main(a)


#metapath = "/home/mherbert/Desktop/test_meta/5877_X.csv"
#result = main(metapath)

#print(result)

# speichern in txt (vorläufig)
'''
open("lang.txt", "w", encoding="utf-8").close()

#funktioniert nicht, ergebnis kopieren und separat abspeichern
def save(result):
    outfile = open("lang.txt", "a", encoding="utf-8")
    for r in result:
        outfile.write("%s\n" % r)
        outfile.close()
#
#t_result = " ".join(result)
#save(result)'''