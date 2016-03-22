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

from syntaq import Syntaq, Heading


class ParagraphTestCase(TestCase):
    
    tests = [
        ("foo bar", "<p>foo bar</p>"),
        ("foo\nbar", "<p>foo bar</p>"),
        ("foo\n\nbar", "<p>foo</p><p>bar</p>"),
        ("foo\n\n\n\nbar", "<p>foo</p><p>bar</p>"),
        ("foo & bar", "<p>foo &amp; bar</p>"),
        ("foo 'bar'", "<p>foo &apos;bar&apos;</p>"),
        ("foo \"bar\"", "<p>foo &quot;bar&quot;</p>"),
        ("foo < bar", "<p>foo &lt; bar</p>"),
        ("foo > bar", "<p>foo &gt; bar</p>"),
        ("I'm **foo** bar", "<p>I&apos;m <strong>foo</strong> bar</p>"),
        ("foo //bar//", "<p>foo <em>bar</em></p>"),
        ("I'm **foo** **bar**", "<p>I&apos;m <strong>foo</strong> <strong>bar</strong></p>"),
        ("//foo// //bar//", "<p><em>foo</em> <em>bar</em></p>"),
        ("I'm **foo** //bar//", "<p>I&apos;m <strong>foo</strong> <em>bar</em></p>"),
        ("I'm **fo\no** //ba\nr//", "<p>I&apos;m <strong>fo o</strong> <em>ba r</em></p>"),
        ("I'm **//foo//** //**bar**//", "<p>I&apos;m <strong><em>foo</em></strong> <em><strong>bar</strong></em></p>"),
        ("I'm **foo\n\nbar", "<p>I&apos;m <strong>foo</strong></p><p>bar</p>"),
        ("//foo\n\nbar", "<p><em>foo</em></p><p>bar</p>"),
        ("I'm **foo\n\nI'm **bar", "<p>I&apos;m <strong>foo</strong></p><p>I&apos;m <strong>bar</strong></p>"),
        ("//foo\n\n//bar", "<p><em>foo</em></p><p><em>bar</em></p>"),
        ("E=mc^^2^^", "<p>E=mc<sup>2</sup></p>"),
        ("H,,2,,SO,,4,,", "<p>H<sub>2</sub>SO<sub>4</sub></p>"),
        ("Here is some code: ``print \"hello, world\"``",
         "<p>Here is some code: <code>print &quot;hello, world&quot;</code></p>"),
        ("Here is some more code: ``print 2 ** 3``", "<p>Here is some more code: <code>print 2 ** 3</code></p>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            assert actual_html == expected_html


class HeadingTestCase(TestCase):

    tests = [
        ("=", "<h1></h1>"),
        ("= ", "<h1></h1>"),
        ("==", "<h2></h2>"),
        ("== ", "<h2></h2>"),
        ("=foo", "<h1>foo</h1>"),
        ("=foo", "<h1>foo</h1>"),
        ("=foo=", "<h1>foo</h1>"),
        ("= foo", "<h1>foo</h1>"),
        ("= foo =", "<h1>foo</h1>"),
        ("= E=mc^2 =", "<h1>E=mc^2</h1>"),
        ("==foo", "<h2>foo</h2>"),
        ("==foo==", "<h2>foo</h2>"),
        ("== foo", "<h2>foo</h2>"),
        ("== foo ==", "<h2>foo</h2>"),
        ("== E=mc^2 ==", "<h2>E=mc^2</h2>"),
        ("=== foo", "<h3>foo</h3>"),
        ("=== foo ===", "<h3>foo</h3>"),
        ("==== foo", "<h4>foo</h4>"),
        ("==== foo ====", "<h4>foo</h4>"),
        ("===== foo", "<h5>foo</h5>"),
        ("===== foo =====", "<h5>foo</h5>"),
        ("====== foo", "<h6>foo</h6>"),
        ("====== foo ======", "<h6>foo</h6>"),
        ("======= foo", "<h6>foo</h6>"),
        ("======= foo =======", "<h6>foo</h6>"),
        ("=== foo ======", "<h3>foo</h3>"),
        ("====== foo ===", "<h6>foo</h6>"),
        ("= foo & bar", "<h1>foo &amp; bar</h1>"),
        ("= foo 'bar'", "<h1>foo &apos;bar&apos;</h1>"),
        ("= foo \"bar\"", "<h1>foo &quot;bar&quot;</h1>"),
        ("= foo < bar", "<h1>foo &lt; bar</h1>"),
        ("= foo > bar", "<h1>foo &gt; bar</h1>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Heading(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(actual_html + " != " + expected_html)
                raise err


class HorizontalRuleTestCase(TestCase):

    tests = [
        ("foo\n---\nbar", "<p>foo --- bar</p>"),
        ("foo\n----\nbar", "<p>foo</p><hr><p>bar</p>"),
        ("foo\n-----\nbar", "<p>foo</p><hr><p>bar</p>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(actual_html + " != " + expected_html)
                raise err


class ListTestCase(TestCase):

    tests = [
        ("* foo\n* bar", "<ul><li>foo</li><li>bar</li></ul>"),
        ("hello\n* foo\n* bar", "<p>hello</p><ul><li>foo</li><li>bar</li></ul>"),
        ("* foo\n* bar\nhello", "<ul><li>foo</li><li>bar</li></ul><p>hello</p>"),
        ("* foo\n* bar\n----", "<ul><li>foo</li><li>bar</li></ul><hr>"),
        ("* foo\n** bar", "<ul><li>foo</li><ul><li>bar</li></ul></ul>"),
        ("* foo\n** bar\n* baz", "<ul><li>foo</li><ul><li>bar</li></ul><li>baz</li></ul>"),
        ("* foo\n* bar\n\n* baz\n* qux", "<ul><li>foo</li><li>bar</li></ul><ul><li>baz</li><li>qux</li></ul>"),
        ("* foo\n* bar\n\n# baz\n# qux", "<ul><li>foo</li><li>bar</li></ul><ol><li>baz</li><li>qux</li></ol>"),
        ("* foo\n# bar\n", "<ul><li>foo</li></ul><ol><li>bar</li></ol>"),
        ("# foo\n* bar\n", "<ol><li>foo</li></ol><ul><li>bar</li></ul>"),
        ("* foo\n## bar\n", "<ul><li>foo</li></ul><ol><ol><li>bar</li></ol></ol>"),
        ("* foo\n*# bar\n", "<ul><li>foo</li><ol><li>bar</li></ol></ul>"),
        ("* foo\n** bar\n", "<ul><li>foo</li><ul><li>bar</li></ul></ul>"),
        ("* foo\n#* bar\n", "<ul><li>foo</li></ul><ol><ul><li>bar</li></ul></ol>"),
        ("## foo\n# bar\n", "<ol><ol><li>foo</li></ol><li>bar</li></ol>"),
        ("*# foo\n# bar\n", "<ul><ol><li>foo</li></ol></ul><ol><li>bar</li></ol>"),
        ("** foo\n# bar\n", "<ul><ul><li>foo</li></ul></ul><ol><li>bar</li></ol>"),
        ("#* foo\n# bar\n", "<ol><ul><li>foo</li></ul><li>bar</li></ol>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(markup + "\n" + actual_html + " != " + expected_html)
                raise err


class PreformattedTestCase(TestCase):

    tests = [
        ("{{{\nfoo\n}}}", "<pre>foo\n</pre>"),
        ("{{{\nfoo\nbar\n}}}", "<pre>foo\nbar\n</pre>"),
        ("{{{\nfoo\n    bar\n}}}", "<pre>foo\n    bar\n</pre>"),
        ("{{{\nfoo    \nbar\n}}}", "<pre>foo    \nbar\n</pre>"),
        ("{{{\nfoo & bar\n}}}", "<pre>foo &amp; bar\n</pre>"),
        ("{{{\nfoo 'bar'\n}}}", "<pre>foo &apos;bar&apos;\n</pre>"),
        ("{{{\nfoo \"bar\"\n}}}", "<pre>foo &quot;bar&quot;\n</pre>"),
        ("{{{\nfoo < bar\n}}}", "<pre>foo &lt; bar\n</pre>"),
        ("{{{\nfoo > bar\n}}}", "<pre>foo &gt; bar\n</pre>"),
        ("{{{\nfoo\n}}}}", "<pre>foo\n</pre>"),
        ("{{{ bar\nfoo\n}}}", "<pre class=\"bar\">foo\n</pre>"),
        ("{{{ bar baz\nfoo\n}}}", "<pre class=\"bar baz\">foo\n</pre>"),
        ("{{{bar\nfoo\n}}}", "<pre class=\"bar\">foo\n</pre>"),
        ("{{{bar baz\nfoo\n}}}", "<pre class=\"bar baz\">foo\n</pre>"),
        ("{{{ bar\nfoo\n}}}", "<pre class=\"bar\">foo\n</pre>"),
        ("{{{ bar     baz\nfoo\n}}}", "<pre class=\"bar baz\">foo\n</pre>"),
        ("{{{  bar\tbaz  \nfoo\n}}}", "<pre class=\"bar baz\">foo\n</pre>"),
        ("{{{\nfoo\n}}}\n{{{\nbar\n}}}", "<pre>foo\n</pre><pre>bar\n</pre>"),
        ("{{{\nfoo\n----\nbar\n}}}", "<pre>foo\n----\nbar\n</pre>"),
        ("{{{\nfoo\n**bar**\n}}}", "<pre>foo\n**bar**\n</pre>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(markup + "\n" + actual_html + " != " + expected_html)
                raise err


class CodeBlockTestCase(TestCase):

    tests = [
        ("```\nfoo\n```", "<pre><ol><li><code>foo\n</code></li></ol></pre>"),
        ("``` foo bar\nbaz\n```", "<pre class=\"foo bar\"><ol><li><code>baz\n</code></li></ol></pre>"),
        ("```\nfoo\nbar\n```", "<pre><ol><li><code>foo\n</code></li><li><code>bar\n</code></li></ol></pre>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(markup + "\n" + actual_html + " != " + expected_html)
                raise err


class BlockQuoteTestCase(TestCase):

    tests = [
        ('"""\nfoo\n"""', '<blockquote>foo\n</blockquote>'),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Syntaq(markup).html
            try:
                assert actual_html == expected_html
            except AssertionError as err:
                print(markup + "\n" + actual_html + " != " + expected_html)
                raise err
