#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from syntaq import Partitioner


class PartitionerTester(unittest.TestCase):

    def test_can_partition_with_marker(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("foo**bar"))
        assert tokens == ["foo", "**", "bar"]

    def test_can_partition_without_marker(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("foo bar"))
        assert tokens == ["foo bar"]

    def test_can_partition_with_marker_at_start(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("**foo bar"))
        assert tokens == ["**", "foo bar"]

    def test_can_partition_with_marker_at_end(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("foo bar**"))
        assert tokens == ["foo bar", "**"]

    def test_can_partition_with_escaped_marker(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("foo~**bar"))
        assert tokens == ["foo", "~**", "bar"]

    def test_can_partition_with_escaped_other(self):
        t = Partitioner("~", "**")
        tokens = list(t.partition("foo~bar"))
        assert tokens == ["foo~bar"]


if __name__ == "__main__":
    unittest.main()
