from markdown_block import BlockType, block_to_block_type, markdown_to_blocks
from markdown import text_to_textnode, codetext_to_textnode
from textnode import text_node_to_html_node
import re
from htmlnode import LeafNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = block_to_html(blocks)
    return htmlnodes


#input : string[], output : HTMLnode[]
def block_to_html(blocks):
    htmlnodes =[]
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.strip()
                text_nodes =text_to_textnode(block)
                child_nodes = []
                for text in text_nodes:
                    child_nodes.append(text_node_to_html_node(text)) 
                parentnode = ParentNode(tag="p", children=child_nodes)
                htmlnodes.append(parentnode)

            case BlockType.HEADING:
                block = block.strip()
                level = len(re.match(r'^(#+)', block).group(0))
                tag = f"h{level}"
                text_nodes = text_to_textnode(block[level:].strip())
                child_nodes = []
                for text in text_nodes:
                    child_nodes.append(text_node_to_html_node(text)) 
                parentnode = ParentNode(tag=tag, children=child_nodes)
                htmlnodes.append(parentnode)
                                
            case BlockType.CODE:
                block = block.strip()

                pattern = re.compile(r'^(?:```|~~~)(\w+)?\n(.*?)(?:\n(?:```|~~~))$', re.DOTALL)
                match = pattern.match(block)

                if match and match.group(1) != None:
                    language = match.group(1).strip()
                    code_content = match.group(2).strip()
                else:
                    language = ""
                    code_content = block[3:-3].strip()

                text_nodes = codetext_to_textnode(code_content)
                child_nodes = []
                for text in text_nodes:
                    child_nodes.append(text_node_to_html_node(text))
                if language != "":
                    parentnode2 = ParentNode(tag="code", children=child_nodes, props={"class": "language-"+language})
                else:
                    parentnode2 = ParentNode(tag="code", children=child_nodes)
                parentnode1 = ParentNode(tag="pre", children=[parentnode2]) # Wrap in a list
                htmlnodes.append(parentnode1)
                htmlnodes.append(parentnode2)

            case BlockType.QUOTE:
                block = block.strip()

                block = block[1:].strip()  # Remove the leading '>'
                block = block.replace("\n> ", "\n")  # Remove leading '>' from subsequent lines
                text_nodes = text_to_textnode(block)
                child_nodes = []
                for text in text_nodes:
                    child_nodes.append(text_node_to_html_node(text))
                parentnode = ParentNode(tag="blockquote", children=child_nodes)
                htmlnodes.append(parentnode)

            case BlockType.HORIZONTAL_RULE:
                parentnode = ParentNode(tag="hr", children=[])
                htmlnodes.append(parentnode)

            # Handle lists

            case BlockType.UNORDERED_LIST:
                block = block.strip()
                items = block.split('\n')
                child_nodes = []
                for item in items:
                    item = item.strip()
                    item = item[2:] if item.startswith("- ") else item  # Remove leading '- '
                    text_nodes = text_to_textnode(item)
                    item_children = []
                    for text in text_nodes:
                        item_children.append(text_node_to_html_node(text))
                    child_nodes.append(ParentNode(tag="li", children=item_children))
                # Create a parent node for the unordered list
                # and add the child nodes to it 
                parentnode = ParentNode(tag="ul", children=child_nodes)
                htmlnodes.append(parentnode)    
            case BlockType.ORDERED_LIST:
                block = block.strip()
                items = block.split('\n')
                child_nodes = []
                for item in items:
                    item = item.strip()
                    match = re.match(r'(\d+)\.\s*(.*)', item)
                    if match:
                        item = match.group(2)  # Get the text after the number and dot
                    else:
                        raise ValueError("Ordered list item does not start with a number followed by a dot")
                    text_nodes = text_to_textnode(item)
                    item_children = []
                    for text in text_nodes:
                        item_children.append(text_node_to_html_node(text))
                    child_nodes.append(ParentNode(tag="li", children=item_children))
                parentnode = ParentNode(tag="ol", children=child_nodes)
                htmlnodes.append(parentnode)
            case _:
                raise ValueError("This Block Type is not supported")

    return htmlnodes



