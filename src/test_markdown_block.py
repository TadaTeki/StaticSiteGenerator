import unittest

from markdown_block import markdown_to_blocks, block_to_block_type, BlockType



class TestSplitNodesDelimiter(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )    

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# Heading 1\n TEST "), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote\n > This is second.\n > This is third"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n - TEHETEHE\n - TEHE4"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n 3. RENSYU"), BlockType.ORDERED_LIST)




if __name__ == "__main__":
    unittest.main()