"""
BINF-259: Write custom merging tool for Pure CN workflow

@author Kyle Hernandez
"""
import pysam
import argparse

def process_vcf(args):
    """
    Main function for merging the PureCN filtered VCF with the raw VCF.
    """
    # Readers
    raw_vcf = pysam.VariantFile(args.raw_vcf)
    purecn_vcf = pysam.VariantFile(args.purecn_vcf)

    # Writer
    mode = 'wz' if args.output_vcf.endswith('.gz') else 'w'
    writer = pysam.VariantFile(args.output_vcf, mode=mode, header=purecn_vcf.header)

    # Merge by reading each variant in raw vcf and looking up in purecn VCF
    total_raw = 0
    total_final = 0
    found_purecn = 0
    try:
        for raw_record in raw_vcf.fetch():
            total_raw += 1
            found = None
            for pcn_record in purecn_vcf.fetch(
                contig=raw_record.chrom,
                start=raw_record.start,
                stop=raw_record.stop
            ):
                if raw_record.pos == pcn_record.pos and \
                   raw_record.alleles == pcn_record.alleles:
                    found = pcn_record.copy()
                    break
            if found:
                total_final += 1
                found_purecn += 1
                # reset id to raw record id 
                found.id = raw_record.id
                writer.write(found)
            else:
                total_final += 1 
                writer.write(raw_record)
    finally:
        raw_vcf.close()
        purecn_vcf.close()
        writer.close()

    # Assert that total_raw == total_final
    assert total_raw == total_final

    # tabix index if bgzipped
    if mode == 'wz':
        tbx = pysam.tabix_index( args.output_vcf, preset='vcf', force=True )

def get_args():
    """Set up argument parser"""
    p = argparse.ArgumentParser('Custom merging of Pure CN VCF with raw VCF')
    p.add_argument('--purecn_vcf', type=str, required=True,
        help = 'Tabix indexed Pure CN VCF')
    p.add_argument('--raw_vcf', type=str, required=True,
        help = 'Unfiltered raw VCF')
    p.add_argument('--output_vcf', type=str, required=True,
        help = 'Output merged VCF (.gz will bgzip and tabix index)')

    return p.parse_args()

if __name__ == '__main__':
    args = get_args()
    process_vcf( args )
