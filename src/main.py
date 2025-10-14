from utils import copy_recursive
from generate import generate_page


def main():
    copy_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
