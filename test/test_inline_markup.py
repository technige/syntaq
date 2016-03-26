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

from syntaq import Text


class InlineMarkupTestCase(TestCase):

    def test_no_content(self):
        line = Text("")
        assert line.html == ""

    def test_no_tags(self):
        line = Text("foo bar")
        assert line.html == "foo bar"

    def test_ampersand(self):
        line = Text("foo & bar")
        assert line.html == "foo &amp; bar"

    def test_entities(self):
        line = Text("foo & ' \" < > bar")
        assert line.html == "foo &amp; &apos; &quot; &lt; &gt; bar"

    def test_strong(self):
        line = Text("foo **bar**")
        assert line.html == "foo <strong>bar</strong>"

    def test_strong_at_start_of_line(self):
        line = Text("**foo** bar")
        assert line.html == "<strong>foo</strong> bar"

    def test_single_asterisks(self):
        line = Text("foo *bar*")
        assert line.html == "foo *bar*"

    def test_em(self):
        line = Text("foo //bar//")
        assert line.html == "foo <em>bar</em>"

    def test_single_slashes(self):
        line = Text("7 / 10")
        assert line.html == "7 / 10"

    def test_code(self):
        line = Text("foo ``bar``")
        assert line.html == "foo <code>bar</code>"

    def test_sup(self):
        line = Text("foo ^^bar^^")
        assert line.html == "foo <sup>bar</sup>"

    def test_sub(self):
        line = Text("foo __bar__")
        assert line.html == "foo <sub>bar</sub>"

    def test_q(self):
        line = Text('foo ""bar""')
        assert line.html == "foo <q>bar</q>"

    def test_nested_tags(self):
        line = Text("foo **//bar//**")
        assert line.html == "foo <strong><em>bar</em></strong>"

    def test_oddly_nested_tags(self):
        line = Text("foo **//**bar**//**")
        assert line.html == "foo <strong><em></em></strong>bar<strong><em></em></strong>"

    def test_code_does_not_nest(self):
        line = Text("foo ``bar ** baz // qux``")
        assert line.html == "foo <code>bar ** baz // qux</code>"

    def test_code_can_contain_ampersand(self):
        line = Text("foo ``bar & baz``")
        assert line.html == "foo <code>bar &amp; baz</code>"

    def test_tag_without_explicit_end(self):
        line = Text("foo **bar")
        assert line.html == "foo <strong>bar</strong>"

    def test_nested_tags_without_explicit_end(self):
        line = Text("foo **//bar**")
        assert line.html == "foo <strong><em>bar</em></strong>"

    def test_image(self):
        line = Text("foo {{bar.png}}")
        assert line.html == 'foo <img src="bar.png">'

    def test_image_with_alt(self):
        line = Text("foo {{bar.png|baz qux}}")
        assert line.html == 'foo <img alt="baz qux" src="bar.png">'

    def test_link(self):
        line = Text("foo [[bar]]")
        assert line.html == 'foo <a href="bar">bar</a>'

    def test_external_link(self):
        line = Text("foo [[http://www.example.com/stuff]]")
        assert line.html == 'foo <a href="http://www.example.com/stuff">http://www.example.com/stuff</a>'

    def test_external_link_with_trailing_slash(self):
        line = Text("foo [[http://www.example.com/stuff/]]")
        assert line.html == 'foo <a href="http://www.example.com/stuff/">http://www.example.com/stuff/</a>'

    def test_unclosed_link(self):
        line = Text("foo [[bar")
        assert line.html == 'foo <a href="bar">bar</a>'

    def test_link_with_description(self):
        line = Text("foo [[bar|description & things]]")
        assert line.html == 'foo <a href="bar">description &amp; things</a>'

    def test_link_with_description_and_markup(self):
        line = Text("foo [[bar|this is an **important** link]]")
        assert line.html == 'foo <a href="bar">this is an <strong>important</strong> link</a>'

    def test_link_with_image_description(self):
        line = Text("foo [[bar|{{image.jpg}}]]")
        assert line.html == 'foo <a href="bar"><img src="image.jpg"></a>'

    def test_unclosed_link_with_image_description(self):
        line = Text("foo [[bar|{{image.jpg")
        assert line.html == 'foo <a href="bar"><img src="image.jpg"></a>'

    def test_link_with_complex_description(self):
        line = Text("[[http://www.example.com/stuff|this is a //really// interesting link --> {{image.jpg}}]]")
        assert line.html == '<a href="http://www.example.com/stuff">this is a <em>really</em> interesting link &rarr; <img src="image.jpg"></a>'

    def test_escaped_asterisks(self):
        line = Text("foo ~** bar")
        assert line.html == "foo ** bar"

    def test_trailing_tilde(self):
        line = Text("foo bar ~")
        assert line.html == "foo bar ~"

    def test_auto_link(self):
        line = Text("foo http://example.com/ bar")
        assert line.html == 'foo <a href="http://example.com/">http://example.com/</a> bar'

    def test_auto_link_with_trailing_dot(self):
        line = Text("foo http://example.com/. bar")
        assert line.html == 'foo <a href="http://example.com/">http://example.com/</a>. bar'

    def test_auto_link_in_angle_brackets(self):
        markup = "foo <http://example.com/> bar"
        expected_html = 'foo &lt;<a href="http://example.com/">http://example.com/</a>&gt; bar'
        actual_html = Text(markup).html
        try:
            assert actual_html == expected_html
        except AssertionError as err:
            print(markup + "\n" + actual_html + " != " + expected_html)
            raise err
