from glob import glob
import csv
# fixed durch csv modul
def integrate(dir,out):
    outfile = open(out,"w",encoding="UTF-8")
    #outfile.write("blog;page;txtlen;url;sitename;author;categories;date;title;hostname;manAnno;scrAnno\n")
    header = ["blog","page","txtlen","url","sitename","author","categories","date","title","hostname","manAnno","scrAnno"]
    writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(header)
    files = "**_X.csv"
    path = "/".join([dir,files])
    all_files = glob(path)
    for metafile in all_files:
        print(metafile)
        with open(metafile,"r",encoding="UTF-8") as f:
            lines = f.read().split("\n")
            for line in lines[1:-1]:
                components = line.split(";")
                if components[9] == "False": # manAnno
                    print("y")
                    components.insert(0,metafile.split("/")[-1].split(".")[0].split("_")[0])
                    #row = ";".join(components)
                    writer.writerow(components)
                else:
                    print("n")

    outfile.close()




integrate("/home/dsturm/Desktop/litblogs/Austauschordner/Skripts/test/clean/", "metaintegration_test_2.csv")
