import cv2
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from tkinter import filedialog
from typing import List, Union
from parser.dstv_object import Dstv_object
from DSTVimage import getObjectImg
import numpy as np
console = Console()

MATCH_THRESHOLD = 0.02

MARKDOWN = """
# DSTV Matcher will take an image and search its database to find the ID of the part in the image

1. First select some DSTV format files of the pieces you have. This will build the database of models.
2. Then select an image and see if a match is found.
3. You can add more models or search more images for a match
4. Enjoy
"""

model_db = []

def print_welcome() -> None:
    console.rule("[bold red]Welcome to DSTV Matcher")
    md = Markdown(MARKDOWN)
    console.print(md)

def print_question() -> str:
    console.print("Enter DB to enter new models to the database or IM to search for a match. q to exit")
    choice = Prompt.ask("Enter choice:", choices=["DB", "IM", "q"])
    return choice

def add_to_model_db(file_names: Union[List[str], None]):
    if (file_names == None):
        return
    for filename in file_names:
        obj = Dstv_object(filename)
        obj_im = getObjectImg(obj)
        # create contour
        contours, hi = cv2.findContours(obj_im,cv2.RETR_CCOMP,1)
        model_db.append({"id":obj.header_info["piece_identification"], "contour":contours, "number_c": len(contours)})

def search_for_match(img_filename):
    img = cv2.imread(img_filename,0)
    ret, thresh = cv2.threshold(img, 127, 255,1)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_CCOMP,1)
    number_c = len(contours)
    for model in model_db:
        if (model["number_c"] != number_c):
            continue
        result = cv2.matchShapes(contours[0],model["contour"][0],1,0.0)
        if (result > MATCH_THRESHOLD):
            continue
        model_av = np.arange(1,model["number_c"])
        match_model = True
        for cnt1 in contours[1:]:
            min_res = 2.0
            pop_index = -1
            for index, model_index in enumerate(model_av):
                cnt2 = model["contour"][model_index]
                result = cv2.matchShapes(cnt1,cnt2,1,0.0)
                if (result < min_res):
                    min_res = result
                    pop_index = index
            if (min_res > MATCH_THRESHOLD):
                match_model = False
                break
            np.delete(model_av, pop_index, 0)
        if (match_model):
            return model["id"]
    return None

def handle_action(action:str) -> None:
    if (action == "DB"):
        nc_file_names = filedialog.askopenfilenames(title="Select NC files", filetypes=[("NC file","*.nc1")])
        add_to_model_db(nc_file_names)
    else:
        img_filename = filedialog.askopenfilename(title="Select Image to search", filetypes=[("PNG","*.png"),("JPEG","*.jpg")])
        id_piece = search_for_match(img_filename)
        if (id_piece == None):
            console.print("[bold red]Not found in db")
        else:
            console.print(f"[bold green]Id is {id_piece}")

if __name__ == "__main__":
    print_welcome()
    choice = print_question()
    while (choice != "q"):
        handle_action(choice)
        choice = print_question()
