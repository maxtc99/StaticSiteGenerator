from textnode import TextType, TextNode
def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node1)
main()