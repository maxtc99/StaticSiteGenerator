from textnode import TextType,TextNode


def main():
    node1 = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
    print(node1)
main()
