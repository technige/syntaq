#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from syntaq import Markup


class ParagraphTester(unittest.TestCase):
    
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
        ("Here is some code: ``print \"hello, world\"``", "<p>Here is some code: <code>print &quot;hello, world&quot;</code></p>"),
        ("Here is some more code: ``print 2 ** 3``", "<p>Here is some more code: <code>print 2 ** 3</code></p>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Markup(markup).to_html()
            assert actual_html == expected_html


class HeadingTester(unittest.TestCase):

    tests = [
        ("=foo", "<h1>foo</h1>"),
        ("=foo\n", "<h1>foo</h1>"),
        ("=foo\nbar", "<h1>foo</h1><p>bar</p>"),
        ("=foo=\nbar", "<h1>foo</h1><p>bar</p>"),
        ("= foo\nbar", "<h1>foo</h1><p>bar</p>"),
        ("= foo =\nbar", "<h1>foo</h1><p>bar</p>"),
        ("= E=mc^2 =\nfoo bar", "<h1>E=mc^2</h1><p>foo bar</p>"),
        ("==foo\nbar", "<h2>foo</h2><p>bar</p>"),
        ("==foo==\nbar", "<h2>foo</h2><p>bar</p>"),
        ("== foo\nbar", "<h2>foo</h2><p>bar</p>"),
        ("== foo ==\nbar", "<h2>foo</h2><p>bar</p>"),
        ("== E=mc^2 ==\nfoo bar", "<h2>E=mc^2</h2><p>foo bar</p>"),
        ("=== foo\nbar", "<h3>foo</h3><p>bar</p>"),
        ("=== foo ===\nbar", "<h3>foo</h3><p>bar</p>"),
        ("==== foo\nbar", "<h4>foo</h4><p>bar</p>"),
        ("==== foo ====\nbar", "<h4>foo</h4><p>bar</p>"),
        ("===== foo\nbar", "<h5>foo</h5><p>bar</p>"),
        ("===== foo =====\nbar", "<h5>foo</h5><p>bar</p>"),
        ("====== foo\nbar", "<h6>foo</h6><p>bar</p>"),
        ("====== foo ======\nbar", "<h6>foo</h6><p>bar</p>"),
        ("======= foo\nbar", "<h6>= foo</h6><p>bar</p>"),
        ("======= foo =======\nbar", "<h6>= foo</h6><p>bar</p>"),
        ("=== foo ======\nbar", "<h3>foo</h3><p>bar</p>"),
        ("====== foo ===\nbar", "<h6>foo</h6><p>bar</p>"),
        ("= foo & bar", "<h1>foo &amp; bar</h1>"),
        ("= foo 'bar'", "<h1>foo &apos;bar&apos;</h1>"),
        ("= foo \"bar\"", "<h1>foo &quot;bar&quot;</h1>"),
        ("= foo < bar", "<h1>foo &lt; bar</h1>"),
        ("= foo > bar", "<h1>foo &gt; bar</h1>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Markup(markup).to_html()
            assert actual_html == expected_html


class HorizontalRuleTester(unittest.TestCase):

    tests = [
        ("foo\n---\nbar", "<p>foo --- bar</p>"),
        ("foo\n----\nbar", "<p>foo</p><hr><p>bar</p>"),
        ("foo\n-----\nbar", "<p>foo</p><hr><p>bar</p>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Markup(markup).to_html()
            assert actual_html == expected_html


class ListTester(unittest.TestCase):

    tests = [
        ("* foo\n* bar", "<ul><li>foo</li><li>bar</li></ul>"),
        ("hello\n* foo\n* bar", "<p>hello</p><ul><li>foo</li><li>bar</li></ul>"),
        ("* foo\n* bar\nhello", "<ul><li>foo</li><li>bar</li></ul><p>hello</p>"),
        ("* foo\n* bar\n----", "<ul><li>foo</li><li>bar</li></ul><hr>"),
        ("* foo\n** bar", "<ul><li>foo</li><ul><li>bar</li></ul></ul>"),
        ("* foo\n** bar\n* baz", "<ul><li>foo</li><ul><li>bar</li></ul><li>baz</li></ul>"),
        ("* foo\n* bar\n\n* baz\n* qux", "<ul><li>foo</li><li>bar</li></ul><ul><li>baz</li><li>qux</li></ul>"),
    ]

    def test_all(self):
        for (markup, expected_html) in self.tests:
            actual_html = Markup(markup).to_html()
            assert actual_html == expected_html


class PreformattedTester(unittest.TestCase):

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
            actual_html = Markup(markup).to_html()
            assert actual_html == expected_html


if __name__ == "__main__":
    unittest.main()
