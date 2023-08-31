import os
from glob import glob
import re
import datetime

from genes_names import GENES_LIST

FNAME_OUT = "./PPMI_RNA.csv"
FNAME_SPORADIC = "./PPMI_RNA_sporadic.csv"
FNAME_HC = "./PPMI_RNA_healthy_controls.csv"

TPM_POS = 3
FILE_DIR = "./"
FILE_REGEXT = "*.BL.*.genes.sf"
FILE_REGISTRY = "./PPMI_Curated_Data_Cut_Public_20230612.csv"

CONST_HC = "Healthy Control"
CONST_SPORADIC = "Sporadic"
CODE_HC = "0"
CODE_SPORADIC = "1"

#GENES_LIST = ["ENSG00000206044", "ENSG00000234312", "ENSGR0000226179", "ENSG00000203864"]

list_temp = []

def find_patno(string, fp):
    PATNO_POS = 1
    SUBGROUP_POS = 4
    REGISTRY_SEPARATOR = ","
    fp.seek(0, os.SEEK_SET)
    for line in fp:
        values = line.split(REGISTRY_SEPARATOR)
        if values[PATNO_POS] == string:
            return values[SUBGROUP_POS]
    return "none"


def find_gene(string, fp):
    global list_temp
    #fp.seek(0, os.SEEK_SET)
    for line in fp:
        if line.startswith(string):
            list_temp = line.split()
            return True
    return False


def main():
    begin = datetime.datetime.now().replace(microsecond=0)
    print("Starting at {}".format(begin))

    fout = open(FNAME_OUT, "w")
    fout_sporadic = open(FNAME_SPORADIC, "w")
    fout_hc = open(FNAME_HC, "w")
    file_regexp = os.path.join(FILE_DIR, FILE_REGEXT)
    file_list = list(glob(file_regexp))
    # print(file_list)
    if len(file_list) == 0:
        print("no file found!")
        exit(-1)

    fregistry = open(FILE_REGISTRY)

    # print headers for the three output files
    print("PATNO, subgroup, ", file=fout, end="")
    for i in range(len(GENES_LIST)):
        print(GENES_LIST[i], file=fout, end="")
        if i != len(GENES_LIST) - 1:
            print(", ", file=fout, end="")
    print("", file=fout)  # add new line

    print("PATNO, ", file=fout_sporadic, end="")
    print("PATNO, ", file=fout_hc, end="")
    for i in range(len(GENES_LIST)):
        print(GENES_LIST[i], file=fout_sporadic, end="")
        print(GENES_LIST[i], file=fout_hc, end="")
        if i != len(GENES_LIST) - 1:
            print(", ", file=fout_sporadic, end="")
            print(", ", file=fout_hc, end="")
    print("", file=fout_sporadic)  # add new line
    print("", file=fout_hc)  # add new line


    nf = 0
    npat = 0
    for fname in file_list:
        nf = nf + 1
        print("Num files: {} ".format(nf), end="")
        re_string = r'\d{4,5}'
        #re_string = r'PPMI-Phase2-IR2\.\d+'
        #re_string = r'd+'
        result = re.search(re_string, fname)
        patno = result.group()
        print(patno + " ", end="")
        patient_type = find_patno(patno, fregistry)
        if patient_type == CONST_HC:
            print(patno + "," + CODE_HC + ", ", file=fout, end="")
            print(patno + ",", file=fout_hc, end="")
        elif patient_type == CONST_SPORADIC:
            print(patno + "," + CODE_SPORADIC + ", ", file=fout, end="")
            print(patno + ",", file=fout_sporadic, end="")
        else:
            # Hyposmia, LRRK2, GBA and other cases
            print("")  # add newline to stdout
            continue
        print(patient_type + "\n")

        npat = npat + 1
        fgenes = open(fname)

        for i in range(len(GENES_LIST)):
            if find_gene(GENES_LIST[i], fgenes):
                print(list_temp[TPM_POS], file=fout, end="")
                if patient_type == CONST_HC:
                    print(list_temp[TPM_POS], file=fout_hc, end="")
                elif patient_type == CONST_SPORADIC:
                    print(list_temp[TPM_POS], file=fout_sporadic, end="")
                else:
                    #bug
                    print("File not well formed: err 1")
                    exit(-1)
            else:
                print("", file=fout, end="")
                if patient_type == CONST_HC:
                    print("", file=fout_hc, end="")
                elif patient_type == CONST_SPORADIC:
                    print("", file=fout_sporadic, end="")
                else:
                    print("File not well formed: err 2")
                    exit(-1)

            if i != len(GENES_LIST) - 1:
                print(", ", file=fout, end="")
                if patient_type == CONST_HC:
                    print(", ", file=fout_hc, end="")
                elif patient_type == CONST_SPORADIC:
                    print(", ", file=fout_sporadic, end="")
                else:
                    #bug
                    print("File not well formed: err 3")
                    exit(-1)

        print("", file=fout)  # add new line
        if patient_type == CONST_HC:
            print("", file=fout_hc)  # add new line
        elif patient_type == CONST_SPORADIC:
            print("", file=fout_sporadic)  # add new line
        else:
            # bug
            print("File not well formed: err 3")
            exit(-1)

        fgenes.close()
        fout.flush()
        fout_sporadic.flush()
        fout_hc.flush()
    fregistry.close()
    fout.close()
    fout_sporadic.close()
    fout_hc.close()
    print("\n")
    print("num files: {}".format(nf))
    print("num patients: {}".format(npat))
    end = datetime.datetime.now().replace(microsecond=0)
    print("\n")
    # print elapsed time
    print("Time spent: {}".format(end-begin))
    print("Program end.")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
