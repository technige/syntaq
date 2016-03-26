#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2016 Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import TestCase

from syntaq import Lexer


class PartitionerTestCase(TestCase):

    def test_can_partition_with_marker(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("foo**bar"))
        assert tokens == ["foo", "**", "bar"]

    def test_can_partition_without_marker(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("foo bar"))
        assert tokens == ["foo bar"]

    def test_can_partition_with_marker_at_start(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("**foo bar"))
        assert tokens == ["**", "foo bar"]

    def test_can_partition_with_marker_at_end(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("foo bar**"))
        assert tokens == ["foo bar", "**"]

    def test_can_partition_with_escaped_marker(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("foo~**bar"))
        assert tokens == ["foo", "~**", "bar"]

    def test_can_partition_with_escaped_other(self):
        t = Lexer("~", "**")
        tokens = list(t.tokens("foo~bar"))
        assert tokens == ["foo~bar"]
