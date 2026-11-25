import unittest
from markdown_blocks import markdown_to_blocks,BlockType, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_excessive_newlines(self):
        md = "First paragraph\n\n\n\nSecond paragraph"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph", "Second paragraph"],
        )

    def test_leading_and_trailing_whitespace(self):
        md = "\n\n  First paragraph  \n\n  Second paragraph  \n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First paragraph", "Second paragraph"],
        )

    def test_single_block(self):
        md = "# A heading"
        self.assertEqual(
            markdown_to_blocks(md),
            ["# A heading"],
        )


class TestBlockToBlockType(unittest.TestCase):


    def test_heading_level_1(self):
        block = "# Heading 1"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_2(self):
        block = "## Heading 2"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_3(self):
        block = "### Heading 3"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_4(self):
        block = "#### Heading 4"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_5(self):
        block = "##### Heading 5"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_6(self):
        block = "###### Heading 6"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_heading_level_7_is_paragraph(self):
        block = "####### Heading 7"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_heading_without_space_is_paragraph(self):
        block = "#Heading"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_code_block(self):
        block = "```\nprint('Hello World')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_multiline_code_block(self):
        block = "```\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_code_block_without_newline_is_paragraph(self):
        block = "```print('Hello')```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_code_block_without_closing_backticks(self):
        block = "```\nprint('Hello')"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_single_line_quote(self):
        block = "> This is a quote"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_multiline_quote(self):
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_quote_without_space(self):
        block = ">First line\n>Second line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_quote_with_mixed_spacing(self):
        block = "> First line\n>Second line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_quote_with_missing_greater_than(self):
        block = "> First line\nSecond line"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


    def test_single_item_unordered_list(self):
        block = "- First item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_multiline_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_without_space(self):
        block = "-First item\n-Second item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_unordered_list_with_mixed_lines(self):
        block = "- First item\nSecond item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


    def test_single_item_ordered_list(self):
        block = "1. First item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_multiline_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_with_double_digit(self):
        block = "\n".join(
            f"{i}. Item {i}" for i in range(1, 12)
        )
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_starting_at_zero(self):
        block = "0. First item\n1. Second item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_starting_at_two(self):
        block = "2. First item\n3. Second item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_with_missing_number(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_with_repeated_number(self):
        block = "1. First item\n1. Second item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_without_space(self):
        block = "1.First item\n2.Second item"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


    def test_simple_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_multiline_paragraph(self):
        block = "First line of text.\nSecond line of text."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_empty_string(self):
        block = ""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

def test_mixed_block_content(self):
    block = "Some paragraph text.\n# Heading"
    self.assertEqual(
        block_to_block_type(block),
        BlockType.PARAGRAPH
    )

class TestMarkdownToHTMLNode(unittest.TestCase):

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and "
            "<code>code</code> here</p></div>",
        )
    def test_codeblock(self):
            md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
            node = markdown_to_html_node(md)

    def test_heading(self):
        md = "## Hello World"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h2>Hello World</h2></div>",
        )

    def test_blockquote(self):
        md = "> This is a quote"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- Apple
- Banana
- Orange"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Apple</li><li>Banana</li><li>Orange</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First
2. Second
3. Third"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
