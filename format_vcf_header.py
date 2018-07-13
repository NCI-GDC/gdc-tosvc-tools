#!/usr/bin/env python
"""
This script formats a VCF file header to contain various GDC-specific metadata attributes:
    * fileDate - the date of the processing
    * center - The NCI Genomic Data Commons (processing center not sequencing)
    * reference - The reference name (GRCh38.d1.vd1.fa)
    * INDIVIDUAL - The patient barcode and case id
    * SAMPLE - the normal/tumor barcode, aliquot uuid and bam uuid (there will be multiple)
"""
import pysam
import argparse
import datetime

def process_vcf(args):
    """
    Takes the command-line arguments and acts as the main wrapper function
    for annotating the GDC VCF headers.
    """
    # Reader
    reader = pysam.VariantFile(args.input_vcf)

    # Load new header
    new_header = build_header( reader, args )

    # Writer based on input file
    mode = 'wz' if args.output_vcf.endswith('gz') else 'w'
    writer = pysam.VariantFile(args.output_vcf, mode=mode, header=new_header)

    # Generate new VCF
    try:
        for record in reader.fetch():
            writer.write(record)
    finally:
        reader.close()
        writer.close()

    # If the output file is bgzipped, we should index it
    if mode == 'wz':
        tbx = pysam.tabix_index( args.output_vcf, preset='vcf', force=True ) 

def build_header( reader, args ):
    """
    Takes the user arguments and the input VCF to generate the GDC
    formatted header entries and returns the header object.
    """
    # First, load the old header, skipping ones that we will update
    lst = []
    for record in reader.header.records:
        if record.key == 'fileDate' or record.key == 'fileformat' or record.key == 'reference': continue
        lst.append(str(record))

    # Add GDC specific metadata
    lst.extend([
      '##fileDate={0}'.format(datetime.date.today().strftime('%Y%m%d')),
      '##center="NCI Genomic Data Commons (GDC)"',
      '##reference={0}'.format(args.reference_name),
      '##INDIVIDUAL=<NAME={0},ID={1}>'.format(args.patient_barcode, args.case_id),
      '##SAMPLE=<ID=TUMOR,NAME={0},ALIQUOT_ID={1},BAM_ID={2}>'.format(
          args.tumor_barcode, args.tumor_aliquot_uuid, args.tumor_bam_uuid)
    ])

    # Initialize new header object
    new_head = pysam.VariantHeader()
    for line in lst:
        new_head.add_line(line)

    # Add samples
    for sample in reader.header.samples:
        new_head.add_sample(sample)

    # Return updated header
    return new_head

def get_args():
    """Function to load the command line arguments."""
    p = argparse.ArgumentParser('Format VCF header according to GDC specs.')
    p.add_argument('--input_vcf', type=str, required=True,
        help='The input VCF file')
    p.add_argument('--output_vcf', type=str, required=True,
        help='The output reheader VCF file')
    p.add_argument('--reference_name', type=str, default='GRCh38.d1.vd1.fa',
        help='reference name to use in header')
    p.add_argument('--patient_barcode', required=True, help='Patient barcode')
    p.add_argument('--case_id', required=True, help='Case ID')
    p.add_argument('--sample_barcode', required=True, help='Tumor barcode')
    p.add_argument('--aliquot_uuid', required=True, help='Tumor aliquot uuid')
    p.add_argument('--bam_uuid', required=True, help='Tumor BAM uuid')
    return p.parse_args()

if __name__ == '__main__':
    args = get_args()
    process_vcf( args )
