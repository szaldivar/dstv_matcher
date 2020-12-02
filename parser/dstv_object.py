from .code_blocks.general import check_for_comment, check_for_block_tag 
from .code_blocks.control import send_control_to_block
from typing import List, Dict, Union

class Dstv_object: 
    
    def __init__(self, filename: str):
        self.header_info: Union[Dict,None] = None
        self.profile_description: Union[Dict,None] = None
        self.holes: Union[List, None] = None
        self.parse_file_contents(filename)

    def parse_file_contents(self, filename: str):
        with open(filename, "r") as file:
            lines: List[str] = file.readlines()
            len_list: int = len(lines)
            index: int = 0
            while (index < len_list):
                line: str = lines[index]
                if (not line):
                    break
                if (check_for_comment(line)):
                    continue
                # the line is not a comment
                # check for block tag
                if (check_for_block_tag(line)):
                    # block tag found, send control to block
                    index = send_control_to_block(index, lines, len_list, self)
                    if (index == -1):
                        return
