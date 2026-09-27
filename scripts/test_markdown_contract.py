import unittest
from validate_knowledge import markdown_errors


class MarkdownContractTests(unittest.TestCase):
    def test_closed_fence(self):
        self.assertEqual(markdown_errors('# Title\n\n```sh\necho ok\n```\n'), [])

    def test_unclosed_fence(self):
        self.assertTrue(markdown_errors('```python\nprint(1)'))

    def test_wrong_closer(self):
        self.assertTrue(markdown_errors('````\n```\n'))

    def test_fence_like_code_is_not_closer(self):
        self.assertTrue(markdown_errors('```\n```not a closing fence'))

    def test_bom(self):
        self.assertTrue(markdown_errors('\ufeff# Heading'))

    def test_nul(self):
        self.assertTrue(markdown_errors('# Heading\x00'))
