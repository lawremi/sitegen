import unittest

from htmlnode import HTMLNode

class TestHTMLNode:
    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {"href": "http://localhost", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="http://localhost" target="_blank"')
        node = HTMLNode("i", "italics")
        self.assertEqual(node.props_to_html(), '')

    def test_repr(self):
        node = HTMLNode("a", None, None, {"href": "http://localhost", "target": "_blank"})
        self.assertEqual(repr(node) == "HTMLNode(a, None, None, {'href': 'http://localhost', 'target': '_blank'})")