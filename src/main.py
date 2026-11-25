import os
import shutil
from textnode import TextNode, TextType
from gencontent import generate_page

def copy_static(source, destination):
    for pr in os.listdir(source):
        if os.path.isfile(os.path.join(source,pr)):
            print("Found a file", os.path.join(source, pr))
            shutil.copy(os.path.join(source, pr), destination)
        else:
            print("Found a folder", os.path.join(destination, pr))
            os.mkdir(os.path.join(destination, pr))
            copy_static(os.path.join(source, pr), os.path.join(destination, pr))
def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_static("static","public")
    generate_page(
            "content/index.md",
            "template.html",
            "public/index.html"
        )

main()
