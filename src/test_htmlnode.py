import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello")

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)

        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello")

        self.assertIn("tag='p'", repr(node))
        self.assertIn("value='Hello'", repr(node))


def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

def test_leaf_to_html_a(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(
        node.to_html(),
        '<a href="https://www.google.com">Click me!</a>'
    )

def test_leaf_to_html_bold(self):
    node = LeafNode("b", "Bold text")
    self.assertEqual(node.to_html(), "<b>Bold text</b>")

def test_leaf_to_html_raw_text(self):
    node = LeafNode(None, "Just plain text")
    self.assertEqual(node.to_html(), "Just plain text")

def test_leaf_to_html_no_value(self):
    node = LeafNode("p", None)
    with self.assertRaises(ValueError):
        node.to_html()

def test_leaf_to_html_multiple_props(self):
    node = LeafNode("a", "Google", {
        "href": "https://google.com",
        "target": "_blank"
    })
    self.assertEqual(
        node.to_html(),
        '<a href="https://google.com" target="_blank">Google</a>'
    )

def test_to_html_with_multiple_children(self):
    children = [
        LeafNode("b", "Bold"),
        LeafNode(None, "Normal"),
        LeafNode("i", "Italic"),
    ]
    parent = ParentNode("p", children)

    self.assertEqual(
        parent.to_html(),
        "<p><b>Bold</b>Normal<i>Italic</i></p>"
    )


def test_to_html_with_nested_children(self):
    grandchild = LeafNode("b", "Bold")
    child = ParentNode("span", [grandchild])
    parent = ParentNode("div", [child])

    self.assertEqual(
        parent.to_html(),
        "<div><span><b>Bold</b></span></div>"
    )


def test_to_html_without_tag(self):
    parent = ParentNode(None, [LeafNode("b", "Bold")])

    with self.assertRaisesRegex(ValueError, "must have a tag"):
        parent.to_html()


def test_to_html_without_children(self):
    parent = ParentNode("div", None)

    with self.assertRaisesRegex(ValueError, "must have children"):
        parent.to_html()


def test_to_html_with_empty_children(self):
    parent = ParentNode("div", [])

    self.assertEqual(parent.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
