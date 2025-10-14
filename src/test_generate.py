import unittest

from generate import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        text = "# This is a title"
        title = extract_title(text)
        self.assertEqual(title, "This is a title")
        text = "Preceding text\n# This is a title"
        title = extract_title(text)
        self.assertEqual(title, "This is a title")

    def test_extract_title_no_title(self):
        text = "This is not a title"
        title = extract_title(text)
        self.assertIsNone(title)
        text = "## This is not a title"
        title = extract_title(text)
        self.assertIsNone(title)
