import unittest

from textnode import TextNode, TextType
from split import split_nodes_delimiter, split_nodes_image, split_nodes_link

class TestSplit(unittest.TestCase):
    def test_split_nodes_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")

    def test_split_nodes_bold_start(self):
        nodes = [TextNode("**This** is bold text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " is bold text")

    def test_split_nodes_bold_end(self):
        nodes = [TextNode("This is bold **text**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is bold ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_spslit_nodes_bold_unbalanced(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
            
    def test_split_nodes_italic(self):
        nodes = [TextNode("This is _italics_ text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italics")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")

    def test_split_nodes_code(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")

    def test_split_nodes_multiple(self):
        nodes = [
            TextNode("This is **bold** and ", TextType.TEXT), 
            TextNode("this is also **bold**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "this is also ")
        self.assertEqual(new_nodes[4].text, "bold")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD)
        
    def test_split_nodes_noop(self):
        nodes = [TextNode("This is text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_no_nodes(self):
        nodes = []
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_image(self):
        nodes = [TextNode("This is ![an image](https://i.imgur.com/zjjcJKZ.png) embedded in text", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "an image")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " embedded in text")
    
    def test_split_nodes_image_no_image(self):
        nodes = [TextNode("This is text without an image", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes[0].text, "This is text without an image")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_nodes_image_multiple(self):
        nodes = [
            TextNode("This is ![an image](https://i.imgur.com/zjjcJKZ.png) and this is ![another image](https://i.imgur.com/sdafJS.png) embedded in text", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].text, "an image")
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and this is ")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].text, "another image")
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/sdafJS.png")
        self.assertEqual(new_nodes[4].text, " embedded in text")
    
    def test_split_nodes_link(self):
        nodes = [TextNode("This is [a link](https://www.google.com) embedded in text", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "a link")
        self.assertEqual(new_nodes[1].url, "https://www.google.com")
        self.assertEqual(new_nodes[2].text, " embedded in text")
    
    def test_split_nodes_link_no_link(self):
        nodes = [TextNode("This is text without a link", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "This is text without a link")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    
    def test_split_nodes_link_multiple(self):
        nodes = [
            TextNode("This is [a link](https://www.google.com) and this is [another link](https://www.bing.com) embedded in text", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].text, "a link")
        self.assertEqual(new_nodes[1].url, "https://www.google.com")
        self.assertEqual(new_nodes[2].text, " and this is ")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].text, "another link")
        self.assertEqual(new_nodes[3].url, "https://www.bing.com")
        self.assertEqual(new_nodes[4].text, " embedded in text")
