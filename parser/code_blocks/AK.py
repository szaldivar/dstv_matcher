from .general import check_for_block_tag, check_for_comment, split_info_lines, read_face_column, dimension_reference
from typing import List, Union, Any

FORMAT: List[int] = [2, 1, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10]
#                    0, 1, 2,  3, 4,  5, 6,  7, 8,  9,10, 11,12, 13,14, 15

def get_type_notch(char: str) -> Union[str,None]:
    aux = {
        " ":"tangential",
        "t":"tangential",
        "w":"hole",
    }
    if (char not in aux):
        return None
    return aux[char]

def read_values(line_info, face, reference, contour: List[Any]) -> bool:
    try:
        x_value = float(line_info[3])
        q_value = float(line_info[5])
        type_notch = get_type_notch(line_info[6])
        if (type_notch == None):
            return True;
        r_value = float(line_info[7])
        weld_v1 = float(line_info[9])
        weld_v2 = float(line_info[11])
        weld_v3 = float(line_info[13])
        weld_v4 = float(line_info[15])
        point = {
            "face": face,
            "reference" : reference,
            "x": x_value,
            "q": q_value,
            "r": r_value,
            "type_notch": type_notch,
            "weld_v1": weld_v1,
            "weld_v2": weld_v2,
            "weld_v3": weld_v3,
            "weld_v4": weld_v4,
        }
        contour.append(point)
        return False
    except:
        return True


def read_line_info(line: str, prevFace: Union[str,None], prevReference: Union[str,None], contour: List[Any]) -> List[Union[str,None]]: 
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
    if (read_values(line_info, face, reference, contour)):
        return [None, None]
    return [face, reference]


def ak_handle(index: int, lines: List[str], len_list: int, obj) -> int:
    prevReference = None
    prevFace = None
    # new contour
    new_contour = []
    while (index < len_list):
        line: str = lines[index]
        if (check_for_comment(line)):
            index += 1
            continue
        if (check_for_block_tag(line)):
            obj.external_contours.append(new_contour)
            return index
        prevFace, prevReference = read_line_info(line, prevFace, prevReference, new_contour)
        if (prevFace == None or prevReference == None):
            return -1
        index += 1
    obj.external_contours.append(new_contour)
    return index
