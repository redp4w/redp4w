import unittest
from sync_latest import START, END, render, update


class LatestFeedTests(unittest.TestCase):
    def setUp(self):
        self.feed = {'posts': [{'date': '2026-09-27', 'title': 'SOC & <analysis>', 'category': 'TryHackMe', 'url': 'https://redp4w.github.io/notes/test/'}]}

    def test_escapes_title(self):
        self.assertIn('SOC &amp; &lt;analysis&gt;', render(self.feed))

    def test_rejects_foreign_hosts(self):
        self.feed['posts'][0]['url'] = 'https://redp4w.github.io.evil.example/pwn'
        with self.assertRaises(ValueError):
            render(self.feed)

    def test_rejects_empty_feed(self):
        with self.assertRaises(ValueError):
            render({'posts': []})

    def test_only_replaces_marked_section(self):
        original = 'before\n' + START + '\nold\n' + END + '\nafter\n'
        result = update(original, render(self.feed))
        self.assertTrue(result.startswith('before\n'))
        self.assertTrue(result.endswith('\nafter\n'))
        self.assertEqual(result.count(START), 1)

    def test_rejects_invalid_markers(self):
        with self.assertRaises(ValueError):
            update('missing markers', render(self.feed))


if __name__ == '__main__':
    unittest.main()
