from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)
        if not images:
            new_nodes.append(node)
            continue
        
        remaining_text = original_text
        for image_alt, image_url in images:
            parts = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = parts[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = original_text
        for link_text, link_url in links:
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = parts[1]
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
            
    return new_nodes