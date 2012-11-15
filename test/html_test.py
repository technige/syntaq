#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from syntaq import HTMLOutputStream


class HTMLOutputStreamTester(unittest.TestCase):

    def test_can_write_text(self):
        out = HTMLOutputStream()
        out.write_text("foo")
        assert str(out) == "foo"

    def test_can_write_text_with_ampersand(self):
        out = HTMLOutputStream()
        out.write_text("foo & bar")
        assert str(out) == "foo &amp; bar"

    def test_can_write_text_with_quotes(self):
        out = HTMLOutputStream()
        out.write_text("foo \"bar\"")
        assert str(out) == "foo &quot;bar&quot;"

    def test_can_write_text_with_apostrophes(self):
        out = HTMLOutputStream()
        out.write_text("foo 'bar'")
        assert str(out) == "foo &apos;bar&apos;"

    def test_can_write_text_with_less_than_symbol(self):
        out = HTMLOutputStream()
        out.write_text("foo < bar")
        assert str(out) == "foo &lt; bar"

    def test_can_write_text_with_greater_than_symbol(self):
        out = HTMLOutputStream()
        out.write_text("foo > bar")
        assert str(out) == "foo &gt; bar"

    def test_can_write_void_tag(self):
        out = HTMLOutputStream()
        out.write_text("foo")
        out.start_tag("br")
        out.write_text("bar")
        assert str(out) == "foo<br>bar"

    def test_can_write_start_and_end_tags(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.write_text("bar")
        out.end_tag("foo")
        assert str(out) == "<foo>bar</foo>"

    def test_can_use_default_end_tag(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.write_text("bar")
        out.end_tag()
        assert str(out) == "<foo>bar</foo>"

    def test_can_write_tag_with_attributes(self):
        out = HTMLOutputStream()
        out.start_tag("foo", {"bar": "baz", "spam": "eggs"})
        out.write_text("qux")
        out.end_tag("foo")
        assert str(out) == '<foo bar="baz" spam="eggs">qux</foo>'

    def test_can_write_tag_with_attributes_containing_entities(self):
        out = HTMLOutputStream()
        out.start_tag("foo", {"bar": "baz", "spam": "bacon & eggs"})
        out.write_text("qux")
        out.end_tag("foo")
        assert str(out) == '<foo bar="baz" spam="bacon &amp; eggs">qux</foo>'

    def test_can_write_nested_elements(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.start_tag("bar")
        out.write_text("baz")
        out.end_tag("bar")
        out.end_tag("foo")
        assert str(out) == "<foo><bar>baz</bar></foo>"

    def test_elements_will_end_in_sequence(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.start_tag("bar")
        out.write_text("baz")
        out.end_tag("foo")
        assert str(out) == "<foo><bar>baz</bar></foo>"

    def test_elements_will_all_end_on_close(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.start_tag("bar")
        out.write_text("baz")
        out.close()
        assert str(out) == "<foo><bar>baz</bar></foo>"

    def test_cannot_write_badly_nested_elements(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.start_tag("bar")
        out.write_text("baz")
        out.end_tag("foo")
        try:
            out.end_tag("bar")
            assert False
        except ValueError:
            assert True

    def test_void_elements_do_not_need_to_end(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.start_tag("bar")
        out.write_text("baz")
        out.start_tag("qux", void=True)
        out.close()
        assert str(out) == "<foo><bar>baz<qux></bar></foo>"

    def test_can_write_raw_html(self):
        out = HTMLOutputStream()
        out.start_tag("foo")
        out.write_text("bar")
        out.end_tag("foo")
        out.write_html("<baz>qux</baz>")
        assert str(out) == "<foo>bar</foo><baz>qux</baz>"


if __name__ == "__main__":
    unittest.main()
