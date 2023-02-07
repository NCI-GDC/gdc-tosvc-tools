#!/usr/bin/env python

from typing import Dict, List, Tuple


def get_info(val: List[str]) -> Tuple[Dict[str, str], Dict[str, str]]:
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


# __END__
