"""
Modify two output files <sample>.csv and <sample>_dnacopy.seg generated by PureCN 1.11.7
"""

import sys
import argparse

parser = argparse.ArgumentParser(description='Modify purecn input files.')
parser.add_argument('--aliquot_id', required=True, help='GDC aliquot_id')
parser.add_argument('--info_file', required=True, help='purecn info file')
parser.add_argument('--seg_file', required=True, help='purecn dnacopy seg file')
parser.add_argument('--modified_info_file', required=True, help='modified purecn info file')
parser.add_argument('--modified_seg_file', required=True, help='modified purecn dnacopy seg file')
args = vars(parser.parse_args())

aliquot_id = args['aliquot_id'].strip()

f1 = open(args['info_file'])
f2 = open(args['modified_info_file'], "w")
tmp = f1.readline().strip().split(",")
f2.write("\t".join(tmp) + "\n")
tmp = f1.readline().strip().split(",")
f2.write("\t".join([aliquot_id] + tmp[1:]) + "\n")
f2.close()
f1.close()

f = open(args['modified_seg_file'], "w")
for line in open(args['seg_file']):
    tmp = line.strip().split(",")
    f.write("\t".join([aliquot_id] + tmp[1:]) + "\n")
f.close()
