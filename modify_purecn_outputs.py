"""
Modify two output files <sample>.csv and <sample>_dnacopy.seg generated by PureCN 1.11.7
following GDC-specs for metadata and content
"""

import sys
import argparse

parser = argparse.ArgumentParser(description='Modify purecn input files.')
parser.add_argument('--sample_id', required=True, help='sample_id')
parser.add_argument('--info_file', required=True, help='purecn info file')
parser.add_argument('--seg_file', required=True, help='purecn dnacopy seg file')
parser.add_argument('--modified_info_file', required=True, help='modified purecn info file')
parser.add_argument('--modified_seg_file', required=True, help='modified purecn dnacopy seg file')
args = vars(parser.parse_args())

sample_id = args['sample_id'].strip()

f1 = open(args['info_file'])
f2 = open(args['modified_info_file'], "w")
tmp = f1.readline().strip().split(",")
tmp1 = []
for t in tmp:
    tmp1.append(t.strip("\""))
f2.write("GDC_Aliquot\t" + "\t".join(tmp1[1:]) + "\n")
tmp = f1.readline().strip().split(",")
tmp1 = []
for t in tmp:
    tmp1.append(t.strip("\""))
f2.write("\t".join([sample_id] + tmp1[1:]) + "\n")
f2.close()
f1.close()

f1 = open(args['seg_file'])
f2 = open(args['modified_seg_file'], "w")
f1.readline()
f2.write("GDC_Aliquot\tChromosome\tStart\tEnd\tNum_Probes\tSegment_Mean\n")
for line in f1:
    tmp = line.strip().split("\t")
    f2.write("\t".join([sample_id] + tmp[1 : len(tmp) - 1]) + "\n")
f2.close()
