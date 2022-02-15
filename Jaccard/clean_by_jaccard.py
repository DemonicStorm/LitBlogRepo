from glob import glob
from nltk.tokenize import wordpunct_tokenize as tok
from itertools import combinations
from nltk.util import everygrams

def jaccard(list1,list2):
    """
    Berechnet Jaccard-Koeffizienten
    :param list1: tokenliste 1
    :param list2: tokenliste 2
    :return: Jaccard-Koeffizient
    """
    s1 = set(list1)
    s2 = set(list2)
    return (len(s1.intersection(s2)) / len(s1.union(s2)))


def main(blogPath,csv=False,dumpToCsv=False, dump_txts=False):
    """
    Vergleicht alle extracted.txt's eines Blog paarweise miteinander um anschließend
    den Jaccard-Koeffizienten zu berechnen. Bei Jaccard-Koeffizient > 0,6 wird
    die .txt mit der geringeren Verzeichnisnr "behalten", bzw. höhere wird in
    dumplist übernommen (Liste der txts, die rausfliegen).
    :param blogPath: Pfad zum Parent-Directory der Webpages eines Blogs, oder angabe einer CSV
    :param csv: Optional: auf True setzen, wenn :blogPath: eine CSV ist
    :param dumpToCsv: Optional: Wenn True, aktualisierung der CSV-Liste mit eingebunden.
    :param dump_txts: Optional: bindet list_txts ein, siehe unten.
    :return: -
    """
    dataPath = "/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5"
    # Optional: Mode: BlogPath ist parent-directory oder csv-datei
    if csv:
        dirNr = blogPath.split("/")[-1].split("_")[0] # Nummer der Hauptverzeichnisses eines Blogs
        print("dir-nr: ", dirNr)
        f_content = open(blogPath, encoding="utf-8").read().split("\n")[1:-1]
        p = ["/".join([dataPath, dirNr, d.split(";")[0], "extracted.txt"]) for d in f_content][:-1]
        print("Anzahl an Pages: ", len(p))

    else:
        gp = "/".join([blogPath, "**/extracted.txt"])
        p = glob(gp)
      
    file_dict = {} # wird in der Schleife befüllt mit "<path>": {tokenset}
    print("tokenizing texts and building tokensets.")
    emptyTxts = []
    for path in p:
        #f = tok(open(path, "r", encoding="utf-8").read()) # tokenisierter Text (nltk), bzw. n-gramisiert in :bridge:
        txt_file = open(path, "r", encoding="utf-8").read()
#### n-gram-setting ####
        bridge = everygrams(txt_file.split(),3,3)
        f = []
        for lst in bridge:
            f.append(" ".join(lst))
        if len(f) > 0: # Hier werden leere txts ausgeschlossen um ZeroDivisionError bei Jaccard zu vermeiden.
            file_dict[path] = set(f)
        else:
            emptyTxts.append(path)
    print("Empty txts: ", emptyTxts)

    pairs = list(combinations(file_dict.keys(),2)) # bildet Paare aus den Webpages um deren Tokensets miteinander zu vergleichen
    pairsNew = []
    print("building Pairs and calculate Jaccard.")
    for a in pairs:
        l = list(a) # trennt die Pair-strings wieder auf
        try:
            vgl = jaccard(file_dict[l[0]],file_dict[l[1]])
        except:
            print("Exception: ", a) 
        l.append(vgl)
        pairsNew.append(tuple(l)) # Pair + Jaccard als triple in Liste
    listOfLists = []
    print("identifying similarities per Webpage.")
    for docpath in p:
        lpwp = [] # list per webpage, alle tupel, die vom selben Ausgangstext ausgehen(tuple[0] selber path)
        for i in sorted(pairsNew, key=lambda x: x[0], reverse=False):
            if i[0] == docpath:
                lpwp.append(i)
        listOfLists.append(lpwp)
    print("writing paths for texts with Jaccard > 0,05 to outfile.")
    dumplist = open("dumplist.txt", "w", encoding="utf-8")
    for txt in emptyTxts:
        dumplist.write(txt + "\n")
    for liste in listOfLists:
        for b in liste:
#### Jaccard-value #####
            if b[2] > 0.05:  #   Hier ist die Aussortierschwelle angegeben 
                if int(b[0].split("/")[7]) > int(b[1].split("/")[7]): # höhere pagenr wird aussortiert.
                    dumplist.write(b[0] + "\n")
                else:
                    dumplist.write(b[1] + "\n")
            else:
                pass
    dumplist.close()
    
    if dump_txts:
        txt_dump_out = input("Bitte Dateinamen inkl. Endung für txt_dumps angeben:")
        list_txts("dumplist.txt",txt_dump_out)
    
    if dumpToCsv:
        print("dumping to csv")
        dump_to_csv("dumplist.txt",blogPath)

def list_txts(dump,out):
    """
    Gibt die Texte der ausgelisteten extracted.txts in einer txt aus.(Augelistet werden "Duplikate")
    :param outfile: gewünschter filename für output-datei
    :return: -
    """
    with open(dump, encoding="utf-8") as f:
        outfile = open(out, "w", encoding="utf-8")
        for line in f:
            c = open(line[:-1], "r", encoding="utf-8").read()
            outfile.write(c + "\n")

        outfile.close()

def dump_to_csv(dump_source, csv_source):
    """
    Nimmt dumplist.txt an und csv-metadatenliste und aktualisiert letztere anhand Jaccard Koeffizient.
    """
    csv = open(csv_source,"r").read().split("\n")
    csv_dict = {}
    for x in csv:
        csv_dict[x.split(";")[0]] = x.split(";")
    with open(dump_source, encoding="utf-8") as f:
        for path in f:
            dir_nr = path.split("/")[8]
            if len(csv_dict[dir_nr]) == 10: # aussortierte pages werden mit "x" gekennzeichnet.
                csv_dict[dir_nr].append("x")
            if len(csv_dict[dir_nr]) == 9:
                csv_dict[dir_nr].append("-")
                csv_dict[dir_nr].append("x")
    file = open(csv_source, "w", encoding="utf-8")
    for values in csv_dict.values():
        outstring = ";".join([val for val in values])
        file.write(outstring + "\n")
    file.close()
    
# main script start

#main("5836_x.csv", csv=True)
#list_txts("dumplist.txt","out5134.txt")

#dump_to_csv("dumplist.txt","5836_x.csv")
#a = glob("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/testkorp/**.csv")
a = glob("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/*.csv")

"""["/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5954_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5957_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5940_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5958_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5941_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5867_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5934_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5977_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5949_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5876_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5943_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5846_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5950_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5966_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5959_x.csv",
     "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/ev_text/5967_x.csv"]"""
path = "/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/"
doclist = ["/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/4866_X.csv",
#"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/4849_X.csv",
"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5822_X.csv",
"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5806_X.csv",
"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5812_X.csv",
"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5601_X.csv",
#"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5779_X.csv",
#"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5505_X.csv",
"/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/unann-> ann/5783_X.csv"]
#exceptions = open("exceptions_Jaccard.txt","a",encoding="utf-8")
for i in doclist:
    try:
        main(i,csv=True,dumpToCsv=True)
    except:
        exceptions.write(i)

#main("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/5840_1.csv", csv=True, dumpToCsv=True)