import unittest
from main import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        md = "# This is a title\n\nThis is a paragraph."
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_invalid(self):
        md = "This is a paragraph without a title."
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("Title is Necessary" in str(context.exception))

class Testgenerate_page(unittest.TestCase):
    def test_generate_page(self):
        from_path = "content/index.md"
        template_path = "template.html"
        dest_path = "public/index.html"

        generate_page(from_path, template_path, dest_path)




if __name__ == '__main__':
    unittest.main()