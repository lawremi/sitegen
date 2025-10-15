import sys
from utils import copy_recursive
from generate import generate_pages_recursive

def main():
    copy_recursive("static", "docs")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
