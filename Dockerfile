FROM python:2

MAINTAINER Nam Sy Vo <vosynam@gmail.com>

RUN mkdir /gdc_tosvc_tools
WORKDIR /gdc_tosvc_tools

COPY filter_mutect_outputs.py .
COPY filter_purecn_outputs.py .
COPY modify_purecn_outputs.py .
COPY format_vcf_header.py .
COPY extract_wig_size.py .
COPY annot_fail_purecn_vcf.py .
COPY filter_vardict_paired_outputs.py .

RUN chmod 755 filter_mutect_outputs.py \
    	      filter_purecn_outputs.py \
	      modify_purecn_outputs.py \
	      format_vcf_header.py \
	      extract_wig_size.py \
              annot_fail_purecn_vcf.py
	      filter_vardict_paired_outputs.py

RUN pip install pysam

