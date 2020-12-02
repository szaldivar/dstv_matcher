
def check_for_comment(line: str) -> bool:
    # a comment is defined as two * in the first two places of the line
    return line[0:2] == "**"

def check_for_block_tag(line: str) -> bool:
    # a control tag has the first two chars of a line different than a space
    if (len(line) >= 2):
        return line[0:2] != "  "
    return False

