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
    pathList = []  # zum befüllen der txtpfade, die angewählt werden sollen
    #blognr = mp.split("/")[-1].split("_")[0] #wählt die Blognummer an, wenn man das Skript durch den gesamten extractions5 ordner laufen lässt
    '''with open("/home/mherbert/Desktop/lang_score_kl0,99_3.csv", encoding="utf-8") as file:   
        for i in file:
            pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5", i.split(";")[0],"extracted.txt"]))
            #print(i)'''
            
    with open("/home/mherbert/Desktop/neu_test_meta/5949_x.csv", encoding="utf-8") as file: 
        for i in file:
            if i.split(";")[-1] != "x":
                '''pfad muss für jeden Blog aktualisiert werden und bis vor das blogverzeichnis gehen und darf nicht mit / enden,
                weil das die joinfunktion automatisch dazwischensetzt. nach pfad steht blognr um durchs ganze Skript laufen zu lassen, ansonsten weglassen'''
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
        #time.sleep(10)  # pause in sek, um request error evtl zu umgehen
            resultList.append(lang_3)
    print(resultList)
    
    '''result = " "
    for i in resultList:
        for j in i: 
            result = result + i 
        result_path = "/home/mherbert/Desktop/litblogs/Austauschordner/Skripts/Sprachanalyse/result_lang_satz.txt"
        with open(result_path, encoding="utf-8") as write_file:
            write_file.write(result)
    #return resultList'''




'''table_csv = ("/home/mherbert/Desktop/lang_score_kl0,99_2.csv", ) #csv mit den Blogeinträgen mit unter 0,99 scores'''

main()
#metapath = "/home/mherbert/Desktop/test_meta/5877_X.csv"
#result = main(metapath)

#print(result)
