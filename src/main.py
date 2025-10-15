from utils import copy_recursive
from generate import generate_pages_recursive


def main():
    copy_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
