
import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#    Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_other_headers(self):
        markdown = """## Subtitle

# Main Title

### Another heading
"""
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_extract_title_no_h1(self):
        markdown = """## Subtitle

### Another heading
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
