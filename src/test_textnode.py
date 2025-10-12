import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node2 = TextNode("This is a different text node", TextType.LINK, "http://localhost")
        node3 = TextNode("This is a different text node", TextType.LINK, "http://localhost")
        self.assertNotEqual(node, node2)
        self.assertEqual(node2, node3)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

if __name__ == "__main__":
    unittest.main()
