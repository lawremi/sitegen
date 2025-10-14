from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode

from split import split_nodes_delimiter, split_nodes_image, split_nodes_link
from blocks import markdown_to_blocks, block_to_block_type, BlockType

import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text.replace("\n", " "), TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_html_nodes(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def list_items_to_html_nodes(text, prefix):
    def strip_prefix(line, prefix):
        return re.sub(f"^{prefix}", "", line).lstrip()
    item_nodes = [text_to_html_nodes(strip_prefix(line, prefix)) for line in text.splitlines()]
    return [ParentNode("li", children) for children in item_nodes]

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", block.strip("`").lstrip())])

    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_html_nodes(block))
        case BlockType.HEADING:
            depth = block.count("#")
            stripped = block.lstrip("#").lstrip()
            return ParentNode("h" + str(depth), text_to_html_nodes(stripped))
        case BlockType.QUOTE:
            stripped = "\n".join(line.lstrip(">").lstrip() for line in block.splitlines())
            return ParentNode("blockquote", text_to_html_nodes(stripped))
        case BlockType.UNORDERED_LIST:
            children = list_items_to_html_nodes(block, "-")
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = list_items_to_html_nodes(block, r'\d+\.')
            return ParentNode("ol", children)
        case _:
            raise ValueError(f"Unknown block type: {block_type}")
        
def markdown_to_html_node(markdown):
    return ParentNode("div", [block_to_html_node(block) for block in markdown_to_blocks(markdown)])
