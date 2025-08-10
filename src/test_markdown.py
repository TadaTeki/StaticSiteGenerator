import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links, text_to_textnode 


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_split_nodes_delimiter_valid1(self):
        nodes = [TextNode("*This* is *italic* 'text'. *So great!*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 5)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This", TextType.ITALIC, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), (" is ", TextType.TEXT, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), ("italic", TextType.ITALIC, None))
        self.assertEqual((result[3].text, result[3].text_type, result[3].url), (" 'text'. ", TextType.TEXT, None))
        self.assertEqual((result[4].text, result[4].text_type, result[4].url), ("So great!", TextType.ITALIC, None))
        
    def test_split_nodes_delimiter_valid2(self):
        nodes = [TextNode("This is 'code' text, including **bold** mark.", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "'", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("code", TextType.CODE, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" text, including **bold** mark.", TextType.TEXT, None))

    def test_split_nodes_delimiter_valid3(self):
        nodes = [TextNode("This is a **bold** text **again!**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is a ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("bold", TextType.BOLD, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" text ", TextType.TEXT, None))
        self.assertEqual((result[3].text, result[3].text_type, result[3].url), ("again!", TextType.BOLD, None))

    def test_split_nodes_delimiter_invalid_text_type(self):
        nodes = [TextNode("This is *bold* text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", TextType.LINK)

    def test_split_nodes_delimiter_text_node(self):
        nodes = [TextNode("This is a text node", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "", TextType.TEXT)
        self.assertEqual(len(result), 1)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is a text node", TextType.TEXT, None))

    def test_split_nodes_delimiter_no_delimiter(self):
        nodes = [TextNode("This is a text without delimiter", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, nodes)

class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_extract_markdown_images_valid(self):
        text = "This is an image ![alt text](http://example.com/image.png) and one more image ![another alt](http://example.com/another_image.png)"
        result = extract_markdown_images(text)
        self.assertListEqual([("alt text", "http://example.com/image.png"), ("another alt", "http://example.com/another_image.png")], result)

    def test_extract_markdown_images_no_images(self):
        text = "This is a text without images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_invalid_text(self):
        with self.assertRaises(ValueError):
            extract_markdown_images(12345)

class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_extract_markdown_links_valid(self):
        text = "This is a link [example](http://example.com) and another [test](http://test.com)"
        result = extract_markdown_links(text)
        self.assertListEqual([("example", "http://example.com"), ("test", "http://test.com")], result)

    def test_extract_markdown_links_no_links(self):
        text = "This is a text without links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_invalid_text(self):
        with self.assertRaises(ValueError):
            extract_markdown_links(12345)

class TestSplitNodesImage(unittest.TestCase):
    
    def test_split_nodes_image_valid1(self):
        nodes = [TextNode("This is an image ![alt text](http://example.com/image.png) and some text", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is an image ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("alt text", TextType.IMAGE, "http://example.com/image.png"))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" and some text", TextType.TEXT, None))

    def test_split_nodes_image_valid2(self):
        nodes = [TextNode("This is an image ![alt text](http://example.com/image.png) some text and additional image ![alt text2](http://example2.com/image2.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is an image ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("alt text", TextType.IMAGE, "http://example.com/image.png"))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" some text and additional image ", TextType.TEXT, None))
        self.assertEqual((result[3].text, result[3].text_type, result[3].url), ("alt text2", TextType.IMAGE, "http://example2.com/image2.png"))

    def test_split_nodes_image_BOLD(self):
        nodes = [TextNode("This is an image ![alt text](http://example.com/image.png) and some text", TextType.BOLD)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, nodes)

    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("This is a text without images", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(len(result), 1)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is a text without images", TextType.TEXT, None))

    def test_split_nodes_image_invalid_node(self):
        with self.assertRaises(ValueError):
            split_nodes_image([12345])  # Invalid node type

class TestSplitNodesLinks(unittest.TestCase): 
    def test_split_nodes_links_valid1(self):
        nodes = [TextNode("This is a link [example](http://example.com) and some text", TextType.TEXT)]
        result = split_nodes_links(nodes)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is a link ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("example", TextType.LINK, "http://example.com"))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" and some text", TextType.TEXT, None))

    def test_split_nodes_links_valid2(self):
        nodes = [TextNode("This is a link [example](http://example.com) and another [test](http://test.com)", TextType.TEXT)]
        result = split_nodes_links(nodes)
        self.assertEqual(len(result), 4)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is a link ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("example", TextType.LINK, "http://example.com"))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" and another ", TextType.TEXT, None))
        self.assertEqual((result[3].text, result[3].text_type, result[3].url), ("test", TextType.LINK, "http://test.com"))

    def test_split_nodes_links_BOLD(self):
        nodes = [TextNode("This is a link [example](http://example.com) and some text", TextType.BOLD)]
        result = split_nodes_links(nodes)
        self.assertEqual(result, nodes)

    def test_split_nodes_links_no_links(self):
        nodes = [TextNode("This is a text without links", TextType.TEXT)]
        result = split_nodes_links(nodes)
        self.assertEqual(result, nodes)

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode_valid(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnode(text)

        self.assertEqual(len(result), 10)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("text", TextType.BOLD, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" with an ", TextType.TEXT, None))
        self.assertEqual((result[3].text, result[3].text_type, result[3].url), ("italic", TextType.ITALIC, None))
        self.assertEqual((result[4].text, result[4].text_type, result[4].url), (" word and a ", TextType.TEXT, None))
        self.assertEqual((result[5].text, result[5].text_type, result[5].url), ("code block", TextType.CODE, None))
        self.assertEqual((result[6].text, result[6].text_type, result[6].url), (" and an ", TextType.TEXT, None))
        self.assertEqual((result[7].text, result[7].text_type, result[7].url), ("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"))
        self.assertEqual((result[8].text, result[8].text_type, result[8].url), (" and a ", TextType.TEXT, None))
        self.assertEqual((result[9].text, result[9].text_type, result[9].url), ("link", TextType.LINK, "https://boot.dev"))

    def test_text_to_textnode_with_bold(self):
        text = "This is **bold** text"
        result = text_to_textnode(text)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("bold", TextType.BOLD, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" text", TextType.TEXT, None))

    def test_text_to_textnode_with_italic(self):
        text = "This is *italic* text"
        result = text_to_textnode(text)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("italic", TextType.ITALIC, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" text", TextType.TEXT, None))

    def test_text_to_textnode_with_code(self):
        text = "This is `code` text"
        result = text_to_textnode(text)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[0].text, result[0].text_type, result[0].url), ("This is ", TextType.TEXT, None))
        self.assertEqual((result[1].text, result[1].text_type, result[1].url), ("code", TextType.CODE, None))
        self.assertEqual((result[2].text, result[2].text_type, result[2].url), (" text", TextType.TEXT, None))

if __name__ == "__main__":
    unittest.main()