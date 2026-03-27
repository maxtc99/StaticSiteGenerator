from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if TextType.TEXT == text_node.text_type:
        return LeafNode(None, text_node.text)
    if TextType.BOLD == text_node.text_type:
        return LeafNode("b", text_node.text)
    if TextType.ITALIC == text_node.text_type:
        return LeafNode("i", text_node.text)
    if TextType.CODE == text_node.text_type:
        return LeafNode("code", text_node.text)
    if TextType.LINK == text_node.text_type:
        properties = {"href": text_node.url}
        return LeafNode("a", text_node.text, properties)
    if TextType.IMAGE == text_node.text_type:
        properties = {"src": text_node.url, "alt": text_node.text}
        return LeafNode("img", "", properties)
    raise Exception(f'Error: invalid text type: {text_node.text_type}')