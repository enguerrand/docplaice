from unittest import TestCase

from main import contains_forbidden_chars


class TestMain(TestCase):

    def test_url_whitelist(self):
        allowed = [
            "",
            "index.md",
            "index",
            "foo",
            "foo/",
            "foo/bar",
            "foo/bar/",
            "foo/bar.md",
            "foo/index.md",
            "fo2/index4.md",
            "/",
            "/index.md",
            "/index",
            "/foo",
            "/foo/",
            "/foo/bar",
            "/foo/bar/",
            "/foo/bar.md",
            "/foo/index.md",
            "/fo2/index4.md",
            "/fo2/index_4.md",
            "/fo2/index-4.md",
        ]
        forbidden = [
            "/.htaccess",
            ".htaccess",
            "/.htuser",
            ".htuser",
            "../../../etc/passwd",
            "/.",
            "/..",
            "/.git",
            "/.git/",
            "/.git/config",
            ".git",
            ".git/",
            ".git/config",
            "/foo[",
            "/foo}",
            ".",
            "..",
            "foo[",
            "foo}",
            "foo/bar/blub/./..",

        ]
        for path in allowed:
            self.assertFalse(contains_forbidden_chars(path))
        for path in forbidden:
            self.assertTrue(contains_forbidden_chars(path))

