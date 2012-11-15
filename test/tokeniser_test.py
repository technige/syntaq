#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from syntaq import Tokeniser


class TokeniserTester(unittest.TestCase):

    def test_can_tokenise_with_marker(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("foo**bar"))
        assert tokens == ["foo", "**", "bar"]

    def test_can_tokenise_without_marker(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("foo bar"))
        assert tokens == ["foo bar"]

    def test_can_tokenise_with_marker_at_start(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("**foo bar"))
        assert tokens == ["**", "foo bar"]

    def test_can_tokenise_with_marker_at_end(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("foo bar**"))
        assert tokens == ["foo bar", "**"]

    def test_can_tokenise_with_escaped_marker(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("foo~**bar"))
        assert tokens == ["foo", "~**", "bar"]

    def test_can_tokenise_with_escaped_other(self):
        t = Tokeniser("~", "**")
        tokens = list(t.tokenise("foo~bar"))
        assert tokens == ["foo~bar"]


if __name__ == "__main__":
    unittest.main()
