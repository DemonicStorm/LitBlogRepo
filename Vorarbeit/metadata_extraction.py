import glob
import json
import gensim

def sorter(n):
    return n["dir_nr"]

meta_out = open("Bloglist.csv", "a", encoding="utf-8") # Übersichtsdatei, welche Blogs schon abgefrühstückt wurden
base_dirs = glob.glob("/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5/*/")
for blog in base_dirs:
    globpath = "/home/dsturm/Desktop/litblogs/Kursmaterial/extraction5/" + blog.split("/")[7] + "/*/metadata.json"
    jsons = glob.glob(globpath) # hier den absoluten Pfad zu den Daten angeben
    outname = jsons[0].split("/")[7] + ".csv"
    out = open(outname, "a", encoding="utf-8") # Übersichtsdatei über einen Blog, analog zur schon Bekannten
    gesamtliste = []
    for metadata in jsons:
        source = open(metadata, "r", encoding="utf-8")
        data = source.read()
        source.close()
        x = json.loads(data)
        x['dir_nr'] = metadata.split("/")[8]
        gesamtliste.append(x)
    fin = sort(gesamtliste, key=sorter, reverse=True)
    for y in fin:   
        #print(metadata)
        #print(x)
        dir_nr, url, sitename, date, categories, autor, titel, hostname = y["dir_nr"], y["url"], y["sitename"], y["date"], y["categories"] , y["author"], y["title"], y["hostname"]
        cat_str = ""
        if len(categories)>0:
            for a in categories:
                cat_str += a+","
        else:
            cat_str = "-"
        if date is not None:
            out.write(str(dir_nr) + ";" + str(url) + ";" + str(sitename) + ";" 
                      + str(date) + ";" + str(cat_str) + ";" +
                      str(autor) + ";" + str(titel) + ";" + str(hostname) + "\n")
        else:
            out.write(str(dir_nr) + ";" + str(url) + ";" + str(sitename) + ";" 
                      + "" + ";" + str(cat_str) + ";" + str(autor) + ";" + 
                      str(titel) + ";" + str(hostname) + "\n")
                            
    meta_out.write(metadata.split("/")[7] + ";" + "\n")
    out.close
meta_out.close()
