import unittest

from textnode import TextNode, TextType
from convert import text_node_to_html_node, text_to_textnodes

class TestConvert(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italics(self):
        node = TextNode("This is an italics text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italics text node")
    
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://localhost")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "http://localhost")
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://localhost")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "http://localhost")
        self.assertEqual(html_node.props["alt"], "This is an image")
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_text_to_textnodes_no_special_nodes(self):
        text = "This is text"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text, "This is text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        