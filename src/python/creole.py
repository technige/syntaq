#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

patterns = [
    (   re.compile(r"&"),
        lambda match: "&amp;"
    ),
    (   re.compile(r"'"),
        lambda match: "&apos;"
    ),
    (   re.compile(r'"'),
        lambda match: "&quot;"
    ),
    (   re.compile(r"<"),
        lambda match: "&lt;"
    ),
    (   re.compile(r">"),
        lambda match: "&gt;"
    ),
    (   re.compile(r"\*\*(.*?)(\*\*|$)"),
        lambda match: "<strong>{0}</strong>".format(*match.groups())
    ),
    (   re.compile(r"//(.*?)(//|$)"),
        lambda match: "<em>{0}</em>".format(*match.groups())
    ),
]

HEADING = [n * "=" for n in range(7)]
HORIZONTAL_RULE = "----"

class Document(object):

    def __init__(self, markup):
        self.blocks = [[]]
        for line in markup.splitlines():
            line = line.strip()
            if line.startswith("="):
                for level in range(6, 0, -1):
                    if line.startswith(HEADING[level]):
                        self.blocks.append([level * "=" + line.strip("=").strip()])
                        break
                self.blocks.append([])
            elif line.startswith(HORIZONTAL_RULE):
                self.blocks.append([HORIZONTAL_RULE])
                self.blocks.append([])
            elif line:
                self.blocks[-1].append(line)
            else:
                self.blocks.append([])
        self.blocks = [" ".join(block) for block in self.blocks if block]
        
    def __xhtml__(self):
        out = []
        for block in self.blocks:
            if block.startswith("="):
                for level in range(6, 0, -1):
                    if block.startswith(HEADING[level]):
                        out.append("<h{0}>{1}</h{0}>".format(level, block[level:]))
                        break
            elif block == HORIZONTAL_RULE:
                out.append("<hr />")
            else:
                out.append("<p>")
                for pattern in patterns:
                    block = pattern[0].sub(pattern[1], block)
                out.append(block)
                out.append("</p>")
        return "".join(out)

def to_xhtml(markup):
    doc = Document(markup)
    print doc.__xhtml__()
    return doc.__xhtml__()

def __test__():
    assert to_xhtml("foo bar") == "<p>foo bar</p>"
    assert to_xhtml("foo\nbar") == "<p>foo bar</p>"
    assert to_xhtml("foo\n\nbar") == "<p>foo</p><p>bar</p>"
    assert to_xhtml("foo\n\n\n\nbar") == "<p>foo</p><p>bar</p>"
    assert to_xhtml("foo & bar") == "<p>foo &amp; bar</p>"
    assert to_xhtml("foo 'bar'") == "<p>foo &apos;bar&apos;</p>"
    assert to_xhtml('foo "bar"') == "<p>foo &quot;bar&quot;</p>"
    assert to_xhtml("foo < bar") == "<p>foo &lt; bar</p>"
    assert to_xhtml("foo > bar") == "<p>foo &gt; bar</p>"
    assert to_xhtml("**foo** bar") == "<p><strong>foo</strong> bar</p>"
    assert to_xhtml("foo //bar//") == "<p>foo <em>bar</em></p>"
    assert to_xhtml("**foo** **bar**") == "<p><strong>foo</strong> <strong>bar</strong></p>"
    assert to_xhtml("//foo// //bar//") == "<p><em>foo</em> <em>bar</em></p>"
    assert to_xhtml("**foo** //bar//") == "<p><strong>foo</strong> <em>bar</em></p>"
    assert to_xhtml("**//foo//** //**bar**//") == "<p><strong><em>foo</em></strong> <em><strong>bar</strong></em></p>"
    assert to_xhtml("**foo\n\nbar") == "<p><strong>foo</strong></p><p>bar</p>"
    assert to_xhtml("//foo\n\nbar") == "<p><em>foo</em></p><p>bar</p>"
    assert to_xhtml("**foo\n\n**bar") == "<p><strong>foo</strong></p><p><strong>bar</strong></p>"
    assert to_xhtml("//foo\n\n//bar") == "<p><em>foo</em></p><p><em>bar</em></p>"
    assert to_xhtml("foo\n---\nbar") == "<p>foo --- bar</p>"
    assert to_xhtml("foo\n----\nbar") == "<p>foo</p><hr /><p>bar</p>"
    assert to_xhtml("foo\n-----\nbar") == "<p>foo</p><hr /><p>bar</p>"
    assert to_xhtml("=foo\nbar") == "<h1>foo</h1><p>bar</p>"
    assert to_xhtml("=foo=\nbar") == "<h1>foo</h1><p>bar</p>"
    assert to_xhtml("= foo\nbar") == "<h1>foo</h1><p>bar</p>"
    assert to_xhtml("= foo =\nbar") == "<h1>foo</h1><p>bar</p>"
    assert to_xhtml("= E=mc^2 =\nfoo bar") == "<h1>E=mc^2</h1><p>foo bar</p>"
    assert to_xhtml("==foo\nbar") == "<h2>foo</h2><p>bar</p>"
    assert to_xhtml("==foo==\nbar") == "<h2>foo</h2><p>bar</p>"
    assert to_xhtml("== foo\nbar") == "<h2>foo</h2><p>bar</p>"
    assert to_xhtml("== foo ==\nbar") == "<h2>foo</h2><p>bar</p>"
    assert to_xhtml("== E=mc^2 ==\nfoo bar") == "<h2>E=mc^2</h2><p>foo bar</p>"
    assert to_xhtml("=== foo\nbar") == "<h3>foo</h3><p>bar</p>"
    assert to_xhtml("=== foo ===\nbar") == "<h3>foo</h3><p>bar</p>"
    assert to_xhtml("==== foo\nbar") == "<h4>foo</h4><p>bar</p>"
    assert to_xhtml("==== foo ====\nbar") == "<h4>foo</h4><p>bar</p>"
    assert to_xhtml("===== foo\nbar") == "<h5>foo</h5><p>bar</p>"
    assert to_xhtml("===== foo =====\nbar") == "<h5>foo</h5><p>bar</p>"
    assert to_xhtml("====== foo\nbar") == "<h6>foo</h6><p>bar</p>"
    assert to_xhtml("====== foo ======\nbar") == "<h6>foo</h6><p>bar</p>"
    assert to_xhtml("======= foo\nbar") == "<h6>foo</h6><p>bar</p>"
    assert to_xhtml("======= foo =======\nbar") == "<h6>foo</h6><p>bar</p>"
    assert to_xhtml("=== foo ======\nbar") == "<h3>foo</h3><p>bar</p>"
    assert to_xhtml("====== foo ===\nbar") == "<h6>foo</h6><p>bar</p>"

if __name__ == "__main__":
    __test__()

