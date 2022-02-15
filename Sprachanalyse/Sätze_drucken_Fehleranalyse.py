import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()

#nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)



'''die txt der Blogeinträge (einzeln) anwählen, welche besonders interessant für nähere Analyse sind 
und Sprache pro Dokument und pro Satz ausgeben lassen'''

def main():
    path = "/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/5949/1824/extracted.txt" #path zu der txt, zu welcher die Sätze ausgegeben werden sollen
    with open(path, encoding="utf-8") as open_file:
        t_content = open_file.read()
        #print(t_content)
    j = 0
    lang = nlp(t_content)
    for i, sent in enumerate(lang.sents): #langdetect über jeden Satz iterieren 
        lang_2 = (sent, sent._.language) #Satz mit in die Ausgabe setzen
        tokenanzahl = len(sent) #Tokenanzahl pro Satz für die relative Anzahl an verschiedenen Sprachen innerhalb eines Blogs
        j = j+1 #für jeden satz eine eigene ID erstellen 
        path_neu = []
        path_neu.append(path + "/" + str(j)) #ID an Path anhängen
        lang_3 = (path_neu, lang_2, tokenanzahl)
        print(lang_3)
    

main()

