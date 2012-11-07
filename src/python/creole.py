#!/usr/bin/env python
# -*- coding: utf-8 -*-

P = ("<p>", "</p>")

def to_html(markup):
    def block(t):
        if tag:
            buf.append(tag[1])
        out.extend(buf)
        if t:
            tag, buf = t, [t[0]]
        else:
            tag, buf = t, []
    out = []
    tag, buf = None, []
    for line in markup.splitlines():
        line = line.strip()
        if tag is None:
            block(P)
            buf.append(line)
    block(None)
    print "".join(out)
    return "".join(out)

def __test__():
    assert to_html("foo **bar**") == "<p>foo <strong>bar</strong></p>"

if __name__ == "__main__":
    __test__()

