FROM python:2

MAINTAINER Nam Sy Vo <vosynam@gmail.com>

RUN mkdir /gdc_tosvc_tools
RUN cd /gdc_tosvc_tools

COPY filter_mutect_outputs.py .
COPY filter_purecn_outputs.py .
COPY modify_purecn_outputs.py .
COPY format_vcf_header.py .
COPY extract_wig_size.py .

RUN chmod 755 filter_mutect_outputs.py \
    	      filter_purecn_outputs.py \
	      modify_purecn_outputs.py \
	      format_vcf_header.py \
	      extract_wig_size.py

RUN pip install pysam
WORKDIR /gdc_tosvc_tools
