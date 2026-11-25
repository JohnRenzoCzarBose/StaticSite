from enum import Enum
from htmlnode import ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    cleaned_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            cleaned_blocks.append(block)

    return cleaned_blocks

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith("#"):
        first_line = lines[0]
        heading_level = len(first_line) - len(first_line.lstrip("#"))
        if (
            1 <= heading_level <= 6
            and first_line[heading_level:heading_level + 1] == " "
        ):
            return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(
        line.startswith(f"{i}. ")
        for i, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            html_node = paragraph_to_html_node(block)

        elif block_type == BlockType.HEADING:
            html_node = heading_to_html_node(block)

        elif block_type == BlockType.CODE:
            html_node = code_to_html_node(block)

        elif block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)

        elif block_type == BlockType.UNORDERED_LIST:
            html_node = unordered_list_to_html_node(block)

        elif block_type == BlockType.ORDERED_LIST:
            html_node = ordered_list_to_html_node(block)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(html_node)

    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children


def paragraph_to_html_node(block):
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)


def heading_to_html_node(block):
    count = 0

    while count < len(block) and block[count] == "#":
        count += 1

    text = block[count:].strip()
    children = text_to_children(text)

    return ParentNode(f"h{count}", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())

    text = " ".join(cleaned_lines)
    children = text_to_children(text)

    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []

    for line in lines:
        text = line[2:].strip()
        li_children = text_to_children(text)

        li_node = ParentNode("li", li_children)
        children.append(li_node)

    return ParentNode("ul", children)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []

    for line in lines:
        text = line.split(".", 1)[1].strip()
        li_children = text_to_children(text)

        li_node = ParentNode("li", li_children)
        children.append(li_node)

    return ParentNode("ol", children)

def code_to_html_node(block):
    text = block[4:-3]
    code_node = TextNode(text, TextType.TEXT)
    code_html_node = text_node_to_html_node(code_node)

    code_parent = ParentNode("code", [code_html_node])
    return ParentNode("pre", [code_parent])
