from . import ST, not_implemented
from typing import List

control_object = {
    "ST": ST.st_handle 
}

def send_control_to_block(index: int, lines: List[str], len_list: int, obj) -> int:
    line = lines[index]
    header: str = line[0:2]
    if (header in control_object):
        return control_object[header](index+1, lines, len_list, obj)
    else:
        return not_implemented.not_implemented_handle(index+1, lines, len_list)
