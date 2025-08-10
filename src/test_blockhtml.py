import unittest

from textnode import ParentNode, LeafNode, text_node_to_html_node
from blockhtml import block_to_html

class TestBlockHTML(unittest.TestCase):

    def test_block_to_html(self):
        blocks = [
            "This is a paragraph\n Second line of the first paragraph\n Third line of the first paragraph",
            "This is another paragraph",
            "This is a paragraph with *italic* text and `code` here\nThis is **bold** on a new line"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<p>This is a paragraph\n Second line of the first paragraph\n Third line of the first paragraph</p>" )
        self.assertEqual(html_nodes[1].to_html(), "<p>This is another paragraph</p>")
        self.assertEqual(html_nodes[2].to_html(), "<p>This is a paragraph with <i>italic</i> text and <code>code</code> here\nThis is <b>bold</b> on a new line</p>")

    def test_block_to_html_with_heading(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<h1>Heading 1</h1>")
        self.assertEqual(html_nodes[1].to_html(), "<h2>Heading 2</h2>")
        self.assertEqual(html_nodes[2].to_html(), "<h3>Heading 3</h3>")

    def test_block_to_html_with_code(self):
        blocks = [
            "```python\nprint('Hello, World!')\n```"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<pre><code class=\"language-python\">print('Hello, World!')</code></pre>")

    def test_block_to_html_with_quote(self):
        blocks = [
            "> This is a quote\n> with multiple lines"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<blockquote>This is a quote\nwith multiple lines</blockquote>")

    def test_block_to_html_with_horizontal_rule(self):
        blocks = [
            "---",
            "***",
            "___"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<hr>")
        self.assertEqual(html_nodes[1].to_html(), "<hr>")
        self.assertEqual(html_nodes[2].to_html(), "<hr>")

    def test_block_to_html_with_unordered_list(self):
        blocks = [
            "- Item 1\n- Item 2\n- Item 3"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def test_block_to_html_with_ordered_list(self):
        blocks = [
            "1. First item\n2. Second item\n3. Third item"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<ol><li>First item</li><li>Second item</li><li>Third item</li></ol>")

    def test_block_to_html_with_mixed_content(self):
        blocks = [
            "This is a paragraph",
            "# Heading",
            "> This is a quote",
            "```python\nprint('Hello')\n```"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes[0].to_html(), "<p>This is a paragraph</p>")
        self.assertEqual(html_nodes[1].to_html(), "<h1>Heading</h1>")
        self.assertEqual(html_nodes[2].to_html(), "<blockquote>This is a quote</blockquote>")
        self.assertEqual(html_nodes[3].to_html(), "<pre><code class=\"language-python\">print('Hello')</code></pre>")

    def test_block_to_html_with_empty_blocks(self):
        blocks = [
            "",
            "   ",
            "\n\n"
        ]

        html_nodes = block_to_html(blocks)
        self.assertEqual(html_nodes, [])


'''
        self.assertEqual(len(html_nodes), 2)
        self.assertIsInstance(html_nodes[0], ParentNode)
        self.assertEqual(html_nodes[0].tag, "p")
        self.assertEqual(len(html_nodes[0].children), 1)
        self.assertIsInstance(html_nodes[0].children[0], LeafNode)
        self.assertEqual(html_nodes[0].children[0].value, "This is a paragraph\n Second line of the first paragraph\n Third line of the first paragraph")

'''


if __name__ == "__main__":
    unittest.main()