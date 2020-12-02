from .general import check_for_block_tag, check_for_comment
from typing import List

def not_implemented_handle(index: int, lines: List[str], len_list: int) -> int:
    while (index < len_list):
        line: str = lines[index]
        if (check_for_comment(line)):
            index += 1
            continue
        if (check_for_block_tag(line)):
            return index
        index += 1
    return index
