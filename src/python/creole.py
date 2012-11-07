#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import sys

entities = [
    ("&", "&amp;"),
    ("'", "&apos;"),
    ('"', "&quot;"),
    ("<", "&lt;"),
    (">", "&gt;"),
]

patterns = [
    (   re.compile(r"\\\\"),
        lambda match: "<br />"
    ),
    (   re.compile(r"\{\{\{\{(.*?)(\}\}\}\})"),
        lambda match: "<code>{0}</code>".format(*match.groups())
    ),
    (   re.compile(r"\{\{\{(.*?)(\}\}\})"),
        lambda match: "<tt>{0}</tt>".format(*match.groups())
    ),
    (   re.compile(r"\*\*(.*?)(\*\*|$)"),
        lambda match: "<strong>{0}</strong>".format(*match.groups())
    ),
    (   re.compile(r"(?<!:)//(.*?)(?<!:)(//|$)"),
        lambda match: "<em>{0}</em>".format(*match.groups())
    ),
    # superscript, e.g. "E=mc^^2^^" (non-standard)
    (   re.compile(r"\^\^(.*?)(\^\^|$)"),
        lambda match: "<sup>{0}</sup>".format(*match.groups())
    ),
    # subscript, e.g. "H,,2,,SO,,4,," (non-standard)
    (   re.compile(r",,(.*?)(,,|$)"),
        lambda match: "<sub>{0}</sub>".format(*match.groups())
    ),
    (   re.compile(r"\[\[([^\|]*?)(\]\]|$)"),
        lambda match: '<a href="{0}">{0}</a>'.format(*match.groups())
    ),
    (   re.compile(r"\[\[([^\|]*?)\|([^\|]*?)(\]\]|$)"),
        lambda match: '<a href="{0}">{1}</a>'.format(*match.groups())
    ),
]

HEADING = [n * "=" for n in range(7)]
HORIZONTAL_RULE = "----"

class Document(object):

    def __init__(self, markup):
        self.blocks = [[]]
        literal = False
        for raw_line in markup.splitlines(True):
            line = raw_line.strip()
            if line.startswith("="):
                for level in range(6, 0, -1):
                    if line.startswith(HEADING[level]):
                        self.blocks.append([level * "=" + line.strip("=").strip()])
                        break
                self.blocks.append([])
            elif line.startswith(HORIZONTAL_RULE):
                self.blocks.append([HORIZONTAL_RULE])
                self.blocks.append([])
            elif line.startswith("{{{{") and "}}}}" not in line:
                self.blocks.append(["{{{{" + " ".join(line[4:].lstrip().split())])
                self.blocks.append([])
                literal = True
            elif line.startswith("}}}}"):
                self.blocks.append(["}}}}"])
                self.blocks.append([])
                literal = False
            elif line.startswith("{{{") and "}}}" not in line:
                self.blocks.append(["{{{" + " ".join(line[3:].lstrip().split())])
                self.blocks.append([])
                literal = True
            elif line.startswith("}}}"):
                self.blocks.append(["}}}"])
                self.blocks.append([])
                literal = False
            else:
                if literal:
                    if self.blocks[-1]:
                        self.blocks[-1][-1] += raw_line
                    else:
                        self.blocks[-1].append(raw_line)
                elif line:
                    self.blocks[-1].append(line)
                else:
                    self.blocks.append([])
        self.blocks = [" ".join(block) for block in self.blocks if block]
        
    def __xhtml__(self, fragment=True):
        out = []
        literal = False
        for block in self.blocks:
            if block.startswith("="):
                for level in range(6, 0, -1):
                    if block.startswith(HEADING[level]):
                        out.append("<h{0}>{1}</h{0}>".format(level, block[level:]))
                        break
            elif block == HORIZONTAL_RULE:
                out.append("<hr />")
            elif block == "{{{{":
                out.append("<pre><code>")
                literal = True
            elif block.startswith("{{{{"):
                out.append('<pre class="{0}"><code>'.format(block[4:]))
                literal = True
            elif block.startswith("}}}}"):
                out.append("</code></pre>")
                literal = False
            elif block == "{{{":
                out.append("<pre>")
                literal = True
            elif block.startswith("{{{"):
                out.append('<pre class="{0}">'.format(block[3:]))
                literal = True
            elif block.startswith("}}}"):
                out.append("</pre>")
                literal = False
            else:
                for char, entity in entities:
                    block = block.replace(char, entity)
                if literal:
                    out.append(block)
                else:
                    out.append("<p>")
                    for pattern in patterns:
                        block = pattern[0].sub(pattern[1], block)
                    out.append(block)
                    out.append("</p>")
        if fragment:
            return "".join(out)
        else:
            return "<!doctype html>\n<html><head></head><body>{0}</body></html>".format("".join(out))

def to_xhtml(markup, fragment=True):
    out = Document(markup).__xhtml__(fragment)
    #print(out)
    return out

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
    assert to_xhtml("E=mc^^2^^") == "<p>E=mc<sup>2</sup></p>"
    assert to_xhtml("H,,2,,SO,,4,,") == "<p>H<sub>2</sub>SO<sub>4</sub></p>"
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
    for arg in sys.argv[1:]:
        if arg.startswith("-"):
            if arg in ("-t", "--test"):
                __test__()
        else:
            f = open(arg)
            try:
                print(to_xhtml(f.read(), fragment=False))
            finally:
                f.close()

