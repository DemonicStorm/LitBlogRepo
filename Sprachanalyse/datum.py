import json

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
                pathList.append("/".join(["/home/mherbert/Desktop/litblogs/Kursmaterial/extraction5/5873", i.split(";")[0],"metadata.json"]))
    print(pathList)


a = "/home/mherbert/Desktop/neu_test_meta/5862_x.csv"
main(a)