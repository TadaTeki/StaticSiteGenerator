from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
import re

text_markers = {
    TextType.TEXT: "",
    TextType.BOLD: "**",
    TextType.ITALIC: ["*","_"],
    TextType.CODE: ["'", "`"],
}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in text_markers or delimiter not in text_markers[text_type]:
        raise ValueError("text_type and delimiter combination is not supported")

    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, (TextNode, LeafNode, ParentNode)):
            raise ValueError("old_node must be an instance of TextNode, LeafNode, or ParentNode")

        if (node.text_type != TextType.TEXT) or (text_type == TextType.TEXT and delimiter == ""): 
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) == 0 or node.text.count(delimiter) == 1:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"TextNode with text '{node.text}' contains an odd number of delimiters '{delimiter}'")
        
        # Split the text into three parts using the delimiter
        parts = node.text.split(delimiter) 
        if len(parts) % 2 != 1:
            raise ValueError(f"TextNode with text '{node.text}' does not split into an odd number of parts with delimiter '{delimiter}'")
        
        # Create a new TextNode for each part
        i = 0
        for i in range(len(parts)):
            if parts[i] != "":
                if i % 2 == 0:
                    # Even index parts are of the specified text_type
                    node_new = TextNode(parts[i], TextType.TEXT, node.url)
                else:
                    # Odd index parts are of TextType.TEXT
                    node_new = TextNode(parts[i], text_type, node.url)                    
                new_nodes.append(node_new) 
            
    return new_nodes


def extract_markdown_links(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    
    match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return match

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, (TextNode, LeafNode, ParentNode)):
            raise ValueError("old_node must be an instance of TextNode, LeafNode, or ParentNode")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)

        if links ==[]:
            new_nodes.append(node)
            continue

        target_text = node.text
        for name, url in links:
            section = target_text.split(f"[{name}]({url})",1)
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT, node.url))
            new_nodes.append(TextNode(name, TextType.LINK, url))
            target_text = section[1]    
        if target_text != "":
            new_nodes.append(TextNode(target_text, TextType.TEXT, node.url))

    return new_nodes

def extract_markdown_images(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    
    match = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)

    return match

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, (TextNode, LeafNode, ParentNode)):
            raise ValueError("old_node must be an instance of TextNode, LeafNode, or ParentNode")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)

        if images ==[]:
            new_nodes.append(node)
            continue

        target_text = node.text
        for name, url in images:
            section = target_text.split(f"![{name}]({url})",1)
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT, node.url))
            new_nodes.append(TextNode(name, TextType.IMAGE, url))
            target_text = section[1]    
        if target_text != "":
            new_nodes.append(TextNode(target_text, TextType.TEXT, node.url))

    return new_nodes

def text_to_textnode(text):
    text = text.strip()
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_image(nodes)

    return nodes

def codetext_to_textnode(text):
    text = text.strip()
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_image(nodes)

    return nodes
