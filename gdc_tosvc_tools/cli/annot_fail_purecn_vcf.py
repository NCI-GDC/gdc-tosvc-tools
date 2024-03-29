#!/usr/bin/env python
"""
Annotate VCF output file generated by Mutect2 and fail to run with PureCN
"""

import gzip
import os
import re
import sys

import click

from gdc_tosvc_tools.__main__ import CLI
from gdc_tosvc_tools.utils import get_info


@click.command(cls=CLI)
@click.option("--purecn-log", "-l", required=True, help="PureCN Log File")
@click.option("--input-vcf", "-i", required=True, help="Input VCF File")
@click.option("--output-vcf", "-o", required=True, help="Annotated Output VCF File")
def main(
    purecn_log: str,
    input_vcf: str,
    output_vcf: str,
) -> None:

    known_error = False
    target_pattern = re.compile(
        r"variants annotated as likely germline \(DB INFO flag\)\."
    )
    germline_percentage = None
    germline_error = False
    seen_error = False
    with open(purecn_log) as f:
        for line in f:
            if "Cannot find valid purity/ploidy solution" in line:
                known_error = True
                break
            match = target_pattern.search(line)
            if match:
                percentage = re.search(r"\(([\d.]+)%\)", line)
                if percentage:
                    germline_percentage = float(percentage.group(1))
            if (
                "error in evaluating the argument 'x' in selecting a method for function 'median': non-numeric argument to mathematical function"
                in line
            ):
                germline_error = True
                break
            error_patterns = [
                "Error in reducer$value.cache[[as.character(idx)]] <- values :",
                "Error in hclust(dist(dx), method = method) :",
            ]
            if any(error_msg in line for error_msg in error_patterns):
                seen_error = True

    if (
        germline_error
        and germline_percentage is not None
        and germline_percentage <= 2.0
    ):
        known_error = True

    if seen_error and germline_percentage is not None and germline_percentage <= 8.0:
        known_error = True

    if known_error:
        if os.path.basename(input_vcf).endswith(".gz"):
            open_fn = gzip
        else:
            open_fn = open  # type: ignore

        filter_add = False
        with open_fn(input_vcf, "r") as input_fh, open(output_vcf, "w") as output_fh:  # type: ignore
            for line in input_fh:
                if line.startswith("#"):
                    if filter_add is False:
                        output_fh.writelines(
                            [
                                '##FILTER=<ID=PASS,Description="Pass all GDC filtering">\n',
                                '##FILTER=<ID=mmq15,Description="median mapping quality less than 15">\n',
                                '##FILTER=<ID=af0.08,Description="alternative allele frequency less than 0.08">\n',
                                "##gdc_filtering_status=PureCN 2.6.4 cannot find valid purity/ploidy solution. These calls have been run through PureCN-GDCfiltration tumor-only variant calling pipeline without PureCN filtering.\n",
                            ]
                        )
                        filter_add = True
                    output_fh.write(line)
                    continue

                val = line.strip().split("\t")
                _, sinfo = get_info(val[7:])
                filter_set = []
                if val[6] != "." and val[6] != "PASS":
                    filter_set = val[6].split(";")
                try:
                    if float(sinfo["MMQ"]) < 15:
                        filter_set.append("mmq15")
                except Exception:
                    pass
                try:
                    if float(sinfo["AF"]) < 0.08:
                        filter_set.append("af0.08")
                except Exception:
                    pass
                if len(filter_set) == 0:
                    output_fh.write("\t".join(val[0:6] + ["PASS"] + val[7:]))
                    output_fh.write("\n")
                else:
                    output_fh.write(
                        "\t".join(val[0:6] + [";".join(filter_set)] + val[7:])
                    )
                    output_fh.write("\n")
    else:
        sys.exit("PureCN failed to unknown issue.")


if __name__ == "__main__":
    main()

# __END__
