FROM python:2

MAINTAINER Nam Sy Vo <vosynam@gmail.com>

RUN mkdir /gdc_tosvc_tools
COPY filter_mutect_outputs.py /gdc_tosvc_tools
COPY filter_purecn_outputs.py /gdc_tosvc_tools
COPY modify_purecn_outputs.py /gdc_tosvc_tools
COPY format_vcf_header.py /gdc_tosvc_tools
COPY extract_wig_size.py /gdc_tosvc_tools

WORKDIR /gdc_tosvc_tools
RUN cd /gdc_tosvc_tools
RUN chmod 755 filter_mutect_outputs.py
RUN chmod 755 filter_purecn_outputs.py
RUN chmod 755 modify_purecn_outputs.py
RUN chmod 755 format_vcf_header.py
RUN chmod 755 extract_wig_size.py