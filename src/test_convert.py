import unittest

from textnode import TextNode, TextType
from convert import text_node_to_html_node, text_to_textnodes, markdown_to_html_node

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

class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_blockquote(self):
        md = """
> This is a quote
> with multiple lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a quote with multiple lines</p></blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is a list
2. with items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>with items</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li></ul></div>",
        )
    
    def test_headings(self):
        md = """
# This is a heading

## This is a subheading

### This is a sub-subheading

#### This is a sub-sub-subheading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a subheading</h2><h3>This is a sub-subheading</h3><h4>This is a sub-sub-subheading</h4></div>",
        )