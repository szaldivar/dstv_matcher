from typing import List, Union

def check_for_comment(line: str) -> bool:
    # a comment is defined as two * in the first two places of the line
    return line[0:2] == "**"

def check_for_block_tag(line: str) -> bool:
    # a control tag has the first two chars of a line different than a space
    if (len(line) >= 2):
        return line[0:2] != "  "
    return False

def split_info_lines(line: str, FORMAT: List[int]) -> List[str]:
    ans: List[str] = []
    past = 0
    for i in FORMAT:
        ans.append(line[past: past + i])
        past += i
    return ans

def read_face_column(char: str) -> Union[str,None]:
    aux = {
        "v":"front",
        "o":"top",
        "h":"behind",
        "u":"bottom",
        " ":"previous"
    }
    if (char not in aux):
        return None
    return aux[char]

def dimension_reference(char: str) -> Union[str,None]:
    aux = {
        " ":"previous",
        "o":"top",
        "s":"axis",
        "u":"bottom",
    }
    if (char not in aux):
        return None
    return aux[char]

