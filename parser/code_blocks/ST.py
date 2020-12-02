from .general import check_for_block_tag, check_for_comment
from typing import List

def st_handle(index: int, lines: List[str], len_list: int, obj) -> int:
    header_index: int = 0
    header_description = [
        "order_identification",
        "drawing_identification",
        "phase_identification",
        "piece_identification",
        "steel_quality",
        "quantity_of_pieces",
        "profile",
        "code_profile",
    ]
    len_header = len(header_description)
    profile_info_description = [
        "length",
        "profile_height",
        "flange_width",
        "flange_thickness",
        "web_thickness",
        "radius",
        "weight_by_meter",
        "painting_surface_by_meter",
        "web_start_cut",
        "web_end_cut",
        "flange_start_cut",
        "flange_end_cut",
        "info1",
        "info2",
        "info3",
        "info4",
    ]
    len_profile_info = len(profile_info_description)
    profile_info_index: int = 0
    header_info = {}
    profile_info = {}
    while (index < len_list):
        line: str = lines[index]
        if (check_for_comment(line)):
            index += 1
            continue
        if (check_for_block_tag(line)):
            obj.header_info = header_info
            obj.profile_description = profile_info
            return index
        if (header_index < len_header):
            header_info[header_description[header_index]] = line.strip()
            header_index += 1
        elif (profile_info_index < len_profile_info):
            profile_info[profile_info_description[profile_info_index]] = line.strip()
            profile_info_index += 1
        else:
            return -1
        index += 1
    obj.header_info = header_info
    obj.profile_description = profile_info
    return index
