import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Hello World", [], {"class": "test"})
        expected = "HTMLNode(tag=div, value=Hello World, children=[], props={'class': 'test'})"
#        print("test_repr",repr(node))
        self.assertEqual(repr(node), expected)

    def test_props_to_html(self):
        node = HTMLNode("span", "Text", [], {"style":"color:red;", "id":"text1"})
        expected = 'style="color:red;" id="text1"'
#        print("test_props_to_html",node.props_to_html())
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_2(self):
        node = HTMLNode("span", "Text", [], {"href": "https://www.google.com","target": "_blank",})
        expected = 'href="https://www.google.com" target="_blank"'
#        print("test_props_to_html_2", node.props_to_html())
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode("p")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_node_to_html(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        expected = '<p class="text">This is a paragraph</p>'
#        print("test_leaf_node_to_html",node.to_html())
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_node_to_html_no_value(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode(None, "This is a text without a tag")
        expected = "This is a text without a tag"
#        print("test_leaf_node_to_html_no_tag",node.to_html())
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren2(self):
        grandchild_node2 = LeafNode("u", "grandchild")
        grandchild_node1 = ParentNode("b", [grandchild_node2])
        child_node = ParentNode("span", [grandchild_node1])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><u>grandchild</u></b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()