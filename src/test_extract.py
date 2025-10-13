import unittest

from extract import extract_markdown_images, extract_markdown_links

class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with multiple images: ![image1](https://i.imgur.com/zjjcJKZ.png) ![image2](https://i.imgur.com/sdafJS.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/sdafJS.png")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with multiple links: [link1](https://www.google.com) [link2](https://www.bing.com)"
        )
        self.assertListEqual([("link1", "https://www.google.com"), ("link2", "https://www.bing.com")], matches)
