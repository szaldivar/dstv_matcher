from .general import check_for_block_tag, check_for_comment, split_info_lines, read_face_column, dimension_reference
from typing import List, Union

FORMAT: List[int] = [2, 1, 1, 10, 1, 10, 1, 10, 1, 9, 1, 1, 9, 1, 9, 1, 9]
#                    0, 1, 2,  3, 4,  5, 6,  7, 8, 9,10,11,12,13,14,15,16

def get_type_hole(char: str) -> Union[str,None]:
    aux = {
        " ":"complete",
        "g":"thread",
        "l":"left_threaded",
        "m":"mark",
        "s":"counter"
    }
    if (char not in aux):
        return None
    return aux[char]

def get_slotted_hole(char: str) -> bool:
    return char == "l"

def read_values(line_info, face, reference, obj) -> bool:
    try:
        x_value = float(line_info[3])
        q_value = float(line_info[5])
        type_hole = get_type_hole(line_info[6])
        if (type_hole == None):
            return True;
        d_value = float(line_info[7])
        if (type_hole == "mark"):
            d_value = 0.0
        slotted_hole = get_slotted_hole(line_info[10])
        if (obj.holes == None):
            obj.holes = []
        to_append = {
            "face": face,
            "reference" : reference,
            "type": type_hole,
            "x": x_value,
            "q": q_value,
            "d": d_value,
            "slotted_hole": slotted_hole
        }
        if (slotted_hole):
            s_width = float(line_info[12])
            s_height = float(line_info[14])
            s_angle = float(line_info[16])
            to_append["s_width"] = s_width
            to_append["s_height"] = s_height
            to_append["s_angle"] = s_angle
        obj.holes.append(to_append)
        return False
    except:
        return True


def read_line_info(line: str, prevFace: Union[str,None], prevReference: Union[str,None], obj) -> List[Union[str,None]]: 
    line_info: List[str] = split_info_lines(line, FORMAT)
    face = read_face_column(line_info[1])
    if (face == "previous"):
        face = prevFace
    if (face == None):
        return [None, None]
    reference = dimension_reference(line_info[4])
    if (reference == "previous"):
        reference = prevReference
    if (reference == None):
        return [None, None]
    if (read_values(line_info, face, reference, obj)):
        return [None, None]
    return [face, reference]


def bo_handle(index: int, lines: List[str], len_list: int, obj) -> int:
    prevReference = None
    prevFace = None
    while (index < len_list):
        line: str = lines[index]
        if (check_for_comment(line)):
            index += 1
            continue
        if (check_for_block_tag(line)):
            return index
        prevFace, prevReference = read_line_info(line, prevFace, prevReference, obj)
        if (prevFace == None or prevReference == None):
            return -1
        index += 1
    return index
