import os
import shutil
import re

from markdown_block import markdown_to_blocks
from blockhtml import block_to_html, markdown_to_html_node

def main():
    print ("hello world")
    source_dir = "static"
    dest_dir = "public"
    content_dir = "content"
    template_path = "template.html"

    cur_dir = os.getcwd()

    abs_source_path = os.path.join(cur_dir, source_dir)
    abs_dest_path = os.path.join(cur_dir, dest_dir)
    abs_content_path = os.path.join(cur_dir, content_dir)
    abs_template_path = os.path.join(cur_dir, template_path)

    delete_tree(abs_dest_path)
    copy_tree(abs_source_path, abs_dest_path)
 
    generate_html_tree(abs_content_path, abs_template_path, abs_dest_path)


def generate_html_tree(abs_content_path, abs_template_path, abs_dest_path):
    for entry in os.listdir(abs_content_path):
        abs_entry_path = os.path.join(abs_content_path,entry)
        abs_tgt_path = os.path.join(abs_dest_path, entry)

        if os.path.isdir(abs_entry_path) == False:
            generate_page(abs_entry_path, abs_template_path, abs_tgt_path.replace(".md", ".html"))
        else:
            os.mkdir(abs_tgt_path)
            generate_html_tree(abs_entry_path, abs_template_path, abs_tgt_path)      

def delete_tree(abs_dest_dir):
    for entry in os.listdir(abs_dest_dir):
        tgt_path = os.path.join(abs_dest_dir,entry)
        if os.path.isdir(tgt_path):
            shutil.rmtree(tgt_path)
        else:
            os.remove(tgt_path)


def copy_tree(abs_source_dir, abs_dest_dir):
    for entry in os.listdir(abs_source_dir):
        if os.path.isdir(os.path.join(abs_source_dir,entry)) == False:
            shutil.copy(os.path.join(abs_source_dir,entry), abs_dest_dir)
        else:
            tgt_path = os.path.join(abs_dest_dir,entry)
            os.mkdir(tgt_path)
            copy_tree(os.path.join(abs_source_dir,entry), tgt_path)

def extract_title(markdown):

    lines = markdown.splitlines()

    if lines and re.match(r'^#\s', lines[0]):
        return lines[0][2:].strip()

    raise Exception("Title is Necessary")    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()
    with open(template_path, "r", encoding="utf-8") as g:
        template = g.read()
    
    conv_htmlnode = markdown_to_html_node(md)
    html_string = ""
    for node in conv_htmlnode:
        html_string += node.to_html() + "\n"
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    print(template)

    with open(dest_path, "w", encoding="utf-8") as h:
        h.write(template)


main()