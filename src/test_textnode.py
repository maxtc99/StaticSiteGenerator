import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq_url(self):
        node1 = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node1, node2)
    
    def test_not_eq_url(self):
        node1 = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Anchor text", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("Anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)
    
if __name__ == "__main__":
    unittest.main()
