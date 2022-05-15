import logging
from math import ceil

log = logging.getLogger(__name__)

def strip_list(in_list: list, cnt_in_every: int) -> list:
    cnt_parts = ceil(len(in_list) / cnt_in_every)
    return [in_list[cnt_in_every * k:cnt_in_every * (k + 1)] for k in range(cnt_parts)]