import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType) -> list:  
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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue       
        extracted_img = extract_markdown_images(old_node.text)     
        og_txt = old_node.text
        if len(extracted_img) == 0:
            new_nodes.append(old_node)
            continue
        for img in extracted_img:
            sections = og_txt.split(f"![{img[0]}]({img[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")         
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            og_txt = sections[1]
        if og_txt != "":
            new_nodes.append(TextNode(og_txt, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list) -> list: 
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue       
        extracted_links = extract_markdown_links(old_node.text)     
        og_txt = old_node.text
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        for link in extracted_links:
            sections = og_txt.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")         
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            og_txt = sections[1]
        if og_txt != "":
            new_nodes.append(TextNode(og_txt, TextType.TEXT))
    return new_nodes    

def extract_markdown_images(text: str) -> list:
    alt_img_url = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return alt_img_url

def extract_markdown_links(text: str) -> list:
    anchor_link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return anchor_link




