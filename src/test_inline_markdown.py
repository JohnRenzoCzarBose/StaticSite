import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitDelimiter(unittest.TestCase):

    def test_code(self):
        node = TextNode("Run `ls` now", TextType.TEXT)

        new_nodes = split_nodes_delimiter(
            [node], "`", TextType.CODE
        )

        expected = [
            TextNode("Run ", TextType.TEXT),
            TextNode("ls", TextType.CODE),
            TextNode(" now", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT
        )

        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT
        )

        new_nodes = split_nodes_delimiter(
            [node], "_", TextType.ITALIC
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)

    def test_non_text_passthrough(self):
        node = TextNode("image.png", TextType.IMAGE, "alt text")

        new_nodes = split_nodes_delimiter(
            [node], "`", TextType.CODE
        )

        self.assertEqual(new_nodes, [node])

    def test_missing_delimiter(self):
        node = TextNode(
            "This has `unclosed code",
            TextType.TEXT
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node], "`", TextType.CODE
            )

    def test_starts_with_delimiter(self):
        node = TextNode("**bold** after", TextType.TEXT)

        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" after", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)

        new_nodes = split_nodes_delimiter(
            [node], "**", TextType.BOLD
        )

        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT)
        ]

        self.assertEqual(new_nodes, expected)


class TestMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        text = (
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        matches = extract_markdown_images(text)

        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ], matches)

    def test_extract_no_images(self):
        matches = extract_markdown_images("This is just regular text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("link", "https://www.boot.dev")],
            matches
        )

    def test_extract_multiple_links(self):
        text = (
            "[to boot dev](https://www.boot.dev) "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)

        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ], matches)

    def test_extract_no_links(self):
        matches = extract_markdown_links("This is just regular text.")
        self.assertListEqual([], matches)

    def test_images_are_not_links(self):
        text = "![image](https://example.com/image.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_links_are_not_images(self):
        text = "[link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_mixed_images_and_links(self):
        text = (
            "![image](https://example.com/image.png) "
            "[link](https://example.com)"
        )

        self.assertListEqual(
            [("image", "https://example.com/image.png")],
            extract_markdown_images(text)
        )

        self.assertListEqual(
            [("link", "https://example.com")],
            extract_markdown_links(text)
        )

    def test_empty_text(self):
        self.assertListEqual([], extract_markdown_images(""))
        self.assertListEqual([], extract_markdown_links(""))



class TestSplitImages(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_single_image(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_no_images(self):
        node = TextNode("Just regular text", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) some text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" some text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_image_at_end(self):
        node = TextNode(
            "Some text ![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("Some text ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_image_preserves_non_text_nodes(self):
        node = TextNode("existing image", TextType.IMAGE, "image.png")

        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![one](one.png)", TextType.TEXT),
            TextNode("Second ![two](two.png)", TextType.TEXT),
        ]

        new_nodes = split_nodes_image(nodes)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "one.png"),
            TextNode("Second ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "two.png"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_image_without_empty_nodes(self):
        node = TextNode(
            "![first](first.png)![second](second.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("first", TextType.IMAGE, "first.png"),
            TextNode("second", TextType.IMAGE, "second.png"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])


class TestSplitLinks(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube",
                TextType.LINK,
                "https://www.youtube.com/@bootdotdev",
            ),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_single_link(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_no_links(self):
        node = TextNode("Just regular text", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

    def test_split_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is great",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is great", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_link_preserves_non_text_nodes(self):
        node = TextNode("existing link", TextType.LINK, "https://example.com")

        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("First [one](one.com)", TextType.TEXT),
            TextNode("Second [two](two.com)", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(nodes)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("one", TextType.LINK, "one.com"),
            TextNode("Second ", TextType.TEXT),
            TextNode("two", TextType.LINK, "two.com"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_links_without_empty_nodes(self):
        node = TextNode(
            "[first](first.com)[second](second.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("first", TextType.LINK, "first.com"),
            TextNode("second", TextType.LINK, "second.com"),
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

    def test_images_are_not_split_as_links(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is just plain text."

        expected = [
            TextNode("This is just plain text.", TextType.TEXT)
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold(self):
        text = "This is **bold** text."

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic(self):
        text = "This is _italic_ text."

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_code(self):
        text = "This is a `code block`."

        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "Look at this ![image](https://example.com/image.png)"

        expected = [
            TextNode("Look at this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "Visit [Boot.dev](https://boot.dev)"

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_all_markdown(self):
        text = (
            "This is **text** with an _italic_ word "
            "and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()
