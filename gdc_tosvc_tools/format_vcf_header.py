#!/usr/bin/env python
"""
This script formats a VCF file header to contain various GDC-specific metadata attributes:
    * fileDate - the date of the processing
    * center - The NCI Genomic Data Commons (processing center not sequencing)
    * reference - The reference name (GRCh38.d1.vd1.fa)
    * INDIVIDUAL - The patient barcode and case id
    * SAMPLE - the sample barcode, aliquot uuid and bam uuid (there will be multiple)
"""
import datetime

import click
import pysam


@click.command()
@click.option("--input_vcf", type=str, required=True, help="The input VCF file")
@click.option(
    "--output_vcf", type=str, required=True, help="The output reheader VCF file"
)
@click.option(
    "--reference_name",
    type=str,
    default="GRCh38.d1.vd1.fa",
    help="reference name to use in header",
)
@click.option("--patient_barcode", required=True, help="Patient barcode")
@click.option("--case_id", required=True, help="Case ID")
@click.option("--sample_barcode", required=True, help="Tumor barcode")
@click.option("--aliquot_uuid", required=True, help="Tumor aliquot uuid")
@click.option("--bam_uuid", required=True, help="Tumor BAM uuid")
def process_vcf(
    input_vcf: str,
    output_vcf: str,
    reference_name: str,
    patient_barcode: str,
    case_id: str,
    sample_barcode: str,
    aliquot_uuid: str,
    bam_uuid: str,
) -> None:
    """
    Takes the command-line arguments and acts as the main wrapper function
    for annotating the GDC VCF headers.
    """
    # Reader
    reader = pysam.VariantFile(input_vcf)

    # Load new header
    new_header = build_header(
        reader,
        reference_name,
        patient_barcode,
        case_id,
        sample_barcode,
        aliquot_uuid,
        bam_uuid,
    )

    # Writer based on input file
    mode = "wb" if output_vcf.endswith("gz") else "w"
    writer = pysam.VariantFile(output_vcf, mode=mode, header=new_header)  # type: ignore

    # Generate new VCF
    try:
        for record in reader.fetch():
            writer.write(record)
    finally:
        reader.close()
        writer.close()

    # If the output file is bgzipped, we should index it
    if mode == "wz":
        pysam.tabix_index(output_vcf, preset="vcf", force=True)


def build_header(
    reader: pysam.VariantFile,
    patient_barcode: str,
    case_id: str,
    reference_name: str,
    aliquot_uuid: str,
    bam_uuid: str,
    sample_barcode: str,
) -> pysam.VariantHeader:
    """
    Takes the user arguments and the input VCF to generate the GDC
    formatted header entries and returns the header object.
    """
    # First, load the old header, skipping ones that we will update
    lst = []
    for record in reader.header.records:
        if (
            record.key == "fileDate"
            or record.key == "fileformat"
            or record.key == "reference"
        ):
            continue
        lst.append(str(record))

    # Add GDC specific metadata
    lst.extend(
        [
            "##fileDate={0}".format(datetime.date.today().strftime("%Y%m%d")),
            '##center="NCI Genomic Data Commons (GDC)"',
            "##reference={0}".format(reference_name),
            "##INDIVIDUAL=<NAME={0},ID={1}>".format(patient_barcode, case_id),
            "##SAMPLE=<ID=TUMOR,NAME={0},ALIQUOT_ID={1},BAM_ID={2}>".format(
                sample_barcode, aliquot_uuid, bam_uuid
            ),
        ]
    )

    # Initialize new header object
    new_head = pysam.VariantHeader()
    for line in lst:
        new_head.add_line(line)

    # Add samples
    for sample in reader.header.samples:
        new_head.add_sample(sample)

    # Return updated header
    return new_head


if __name__ == "__main__":
    process_vcf()

# __END__
