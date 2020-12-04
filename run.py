from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
console = Console()

MARKDOWN = """
# DSTV Matcher will take an image and search its database to find the ID of the part in the image

1. First select some DSTV format files of the pieces you have. This will build the database of models.
2. Then select an image and see if a match is found.
3. You can add more models or search more images for a match
4. Enjoy
"""

def print_welcome():
    console.rule("[bold red]Welcome to DSTV Matcher")
    md = Markdown(MARKDOWN)
    console.print(md)

def print_question():
    console.print("Enter DB to enter new models to the database or IM to search for a match")
    choice = Prompt.ask("Enter choice:", choices=["DB", "IM"])
    print(choice)

if __name__ == "__main__":
    print_welcome()
    print_question()
