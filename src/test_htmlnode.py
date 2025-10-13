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

class TestLeafNode:
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(node,'<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None).to_html()

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode:
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_tag_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()

    def test_to_html_children_none(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    
    def test_to_html_children_empty(self):
        node = ParentNode("div", []).to_html()
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')
