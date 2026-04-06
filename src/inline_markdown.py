import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    new_nodes = []
    for old_node in old_nodes:     
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue           
        split_nodes=[]
        sections = old_node.text.split(delimiter)    
        if len(sections) % 2 == 0:   # a properly formatted section will always result in an uneven list. e.g: **bolded** == ["","bolded",""] Therefore, 3 % 2 == 1
            raise ValueError("invalid markdown, formatted section not closed") # "**bolded" = ["","bolded"]  because .split() splits around the delimiter
        for i, section in enumerate(sections): 
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))  
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes: list) -> list: 
    new_nodes = []
    for old_node in old_nodes:
        extracted_list = extract_markdown_images(old_node.text)
        counter = 0
        og_txt = old_node.text
        for ex_tuple in extracted_list:
            counter += 1
            sections = og_txt.split(f"![{ex_tuple[0]}]({ex_tuple[1]})", 1)
            og_txt = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(ex_tuple[0], TextType.IMAGE, ex_tuple[1]))
            if len(extracted_list) == counter and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_list = extract_markdown_links(old_node.text)
        if extracted_list == None:
            return [old_nodes]
        counter = 0
        og_txt = old_node.text
        for ex_tuple in extracted_list:
            counter += 1
            sections = og_txt.split(f"[{ex_tuple[0]}]({ex_tuple[1]})", 1)
            og_txt = sections[1]
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(ex_tuple[0], TextType.LINK, ex_tuple[1]))
            if len(extracted_list) == counter and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes    

def extract_markdown_images(text: str) -> list:
    alt_img_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_img_url

def extract_markdown_links(text: str) -> list:
    anchor_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return anchor_link

def main():
    node = TextNode("This is text with a [link](https://www.google.com) and another [second link](https://www.youtube.com)", TextType.TEXT)
    print(split_nodes_link([node]))
main()