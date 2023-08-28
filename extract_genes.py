import os
from glob import glob
import re
import datetime

READ_POS = 4
FILE_DIR = "./sf"
FILE_REGEXT = "*.BL.*.genes.sf"
FILE_REGISTRY = "./PPMI_Curated_Data_Cut_Public_20230612.csv"

GENES_LIST = ["ENSG00000206044", "ENSG00000234312", "ENSGR0000226179", "ENSG00000203864"]

list_temp = []

def find_patno(string, fp):
    PATNO_POS = 1
    SUBGROUP_POS = 4
    REGISTRY_SEPARATOR = ","
    for line in fp:
        values = line.split(REGISTRY_SEPARATOR)
        if values[PATNO_POS] == string:
            return values[SUBGROUP_POS]
    return "none"


def find_gene(string, fp):
    global list_temp
    for line in fp:
        if line.startswith(string):
            list_temp = line.split()
            return True
            break
    return False


def main():
    begin = datetime.datetime.now().replace(microsecond=0)
    print("Starting at {}".format(begin))

    fout = open("out.txt", "w")
    file_regexp = os.path.join(FILE_DIR, FILE_REGEXT)
    file_list = list(glob(file_regexp))
    # print(file_list)
    if len(file_list) == 0:
        print("no file found!")
        exit(-1)

    fregistry = open(FILE_REGISTRY)

    print("PATNO, subgroup, ", file=fout, end="")
    for i in range(len(GENES_LIST)):
        print(GENES_LIST[i], file=fout, end="")
        if i != len(GENES_LIST) - 1:
            print(", ", file=fout, end="")
    print("", file=fout)  # add new line

    for fname in file_list:
        print(".", end="")
        re_string = r'\d{4}'
        result = re.search(re_string, fname)
        patno = result.group()
        res = find_patno(patno, fregistry)
        if res == "none":
            continue
        if res == "Healthy Control":
            print(patno + ", 0, ", file=fout, end="")
        elif res == "Sporadic":
            print(patno + ", 1, ", file=fout, end="")
        else:
            continue

        fgenes = open(fname)

        for i in range(len(GENES_LIST)):
            fgenes.seek(0, os.SEEK_SET)
            if find_gene(GENES_LIST[i], fgenes):
                print(list_temp[READ_POS], file=fout, end="")
            else:
                print("0", file=fout, end="")
            if i != len(GENES_LIST) - 1:
                print(", ", file=fout, end="")
        print("", file=fout)  # add new line
        fgenes.close()
    fregistry.close()
    fout.close()
    end = datetime.datetime.now().replace(microsecond=0)
    print("\n")
    print("Time spent: {}".format(begin-end))
    print("Program end.")
    # print elapsed time


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
