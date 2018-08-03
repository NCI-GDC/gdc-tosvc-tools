"""
Filter VCF output file generated by Mutect2
"""

import sys
import argparse

def get_info(val):
    info, sinfo = {}, {}
    for v in val[0].split(";"):
        tmp1 = v.split("=")
        if len(tmp1) == 2:
            info[tmp1[0]] = tmp1[1]
    tmp2 = val[1].split(":")
    tmp3 = val[2].split(":")
    for i in range(len(tmp2)):
        sinfo[tmp2[i]] = tmp3[i]
    return info, sinfo

parser = argparse.ArgumentParser(description='Modify purecn input files.')
parser.add_argument('-i', '--input_vcf', type=str, required=True, help='purecn input vcf file')
parser.add_argument('-o', '--output_vcf', type=str, required=True, help='filtered output vcf file')
args = vars(parser.parse_args())
input_fn = args['input_vcf']
output_fn = args['output_vcf']

f1 = open(input_fn)
f2 = open(output_fn, "w")
filter_add = False
for line in f1:
    if line[0] == "#":
        if filter_add == False:
            f2.write("##FILTER=<ID=PASS,Description=\"Pass all GDC filtering\">\n")
            f2.write("##FILTER=<ID=mmq15,Description=\"median mapping quality less than 15\">\n")
            f2.write("##FILTER=<ID=af0.08,Description=\"alternative allele frequency less than 0.08\">\n")
            f2.write("##gdc_filtering_status=These calls have not been filtered by PureCN because PureCN NormalDB is not available for this capture kit.\n")
            filter_add = True
        f2.write(line)
        continue

    val = line.strip().split("\t")
    info, sinfo = get_info(val[7:])
    filter_set = []
    if val[6] != "." and val[6] != "PASS":
        filter_set = val[6].split(";")
    try:
        if float(sinfo["MMQ"]) < 15:
            filter_set.append("mmq15")
    except:
        pass
    try:
        if float(sinfo["AF"]) < 0.08:
            filter_set.append("af0.08")
    except:
        pass
    if len(filter_set) == 0:
        f2.write("\t".join(val[0:6] + ["PASS"] + val[7:]) + "\n")
    else:
        f2.write("\t".join(val[0:6] + [";".join(filter_set)] + val[7:]) + "\n")

f1.close()
f2.close()
