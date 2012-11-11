#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re

HEADING = re.compile(r"^(={1,6})\s*(.*[^=\s])\s*=*")
HORIZONTAL_RULE = re.compile(r"^(-{4})")
ORDERED_LIST = re.compile(r"^(#+)\s*(.*)")
PREFORMATTED = re.compile(r"^(\{\{\{)(?!\{)\s*([-\s\w]*)", re.UNICODE)
PREFORMATTED_CODE = re.compile(r"^(\{\{\{\{)(?!\{)\s*([-\s\w]*)", re.UNICODE)
UNORDERED_LIST = re.compile(r"^(\*+)\s*(.*)")

END_OF_PREFORMATTED = re.compile(r"^\s*(\}\}\})")

entities = [
    ("&", "&amp;"),
    ("'", "&apos;"),
    ('"', "&quot;"),
    ("<", "&lt;"),
    (">", "&gt;"),
]



elements = [
    (   re.compile(r"\\\\"),
        lambda match: "<br />"
    ),
    (   re.compile(r"\{\{\{\{(.*?)(\}\}\}\})"),
        lambda match: "<code>{0}</code>".format(*match.groups())
    ),
    (   re.compile(r"\{\{\{(.*?)(\}\}\})"),
        lambda match: "<tt>{0}</tt>".format(*match.groups()) # WRONG! should be nowiki
    ),
    (   re.compile(r"\{\{([^\|]*?)(\}\}|$)"),
        lambda match: "<img src=\"{0}\" />".format(*match.groups())
    ),
    (   re.compile(r"\{\{([^\|]*?)\|([^\|]*?)(\}\}|$)"),
        lambda match: "<img src=\"{0}\" alt=\"{1}\" />".format(*match.groups())
    ),
    # monospace
    (   re.compile(r"##(.*?)(##|$)"),
        lambda match: "<tt>{0}</tt>".format(*match.groups())
    ),
    (   re.compile(r"\*\*(.*?)(\*\*|$)"),
        lambda match: "<strong>{0}</strong>".format(*match.groups())
    ),
    (   re.compile(r"(?<!:)//(.*?)(?<!:)(//|$)"),
        lambda match: "<em>{0}</em>".format(*match.groups())
    ),
    # superscript, e.g. "E=mc^^2^^"
    (   re.compile(r"\^\^(.*?)(\^\^|$)"),
        lambda match: "<sup>{0}</sup>".format(*match.groups())
    ),
    # subscript, e.g. "H,,2,,SO,,4,,"
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

class Document(object):

    def __init__(self, markup):
        self.blocks = []
        block, params, lines = None, None, []
        for line in markup.splitlines(True):
            if block in (PREFORMATTED, PREFORMATTED_CODE):
                end_of_preformatted = END_OF_PREFORMATTED.match(line)
                if end_of_preformatted:
                    self._append_block(block, params, lines)
                    block, params, lines = None, None, []
                else:
                    lines.append(line)
            else:
                line = line.strip()
                heading = HEADING.match(line)
                horizontal_rule = HORIZONTAL_RULE.match(line)
                ordered_list = ORDERED_LIST.match(line)
                preformatted = PREFORMATTED.match(line)
                preformatted_code = PREFORMATTED_CODE.match(line)
                unordered_list = UNORDERED_LIST.match(line)
                if heading:
                    self._append_block(block, params, lines)
                    block, params, lines = None, None, []
                    self.blocks.append((HEADING, len(heading.group(1)), [heading.group(2)]))
                elif horizontal_rule:
                    self._append_block(block, params, lines)
                    block, params, lines = None, None, []
                    self.blocks.append((HORIZONTAL_RULE, None, None))
                elif ordered_list:
                    if block is ORDERED_LIST:
                        params.append(len(ordered_list.group(1)))
                        lines.append(ordered_list.group(2))
                    else:
                        self._append_block(block, params, lines)
                        block, params, lines = ORDERED_LIST, [len(ordered_list.group(1))], [ordered_list.group(2)]
                elif preformatted:
                    self._append_block(block, params, lines)
                    block, params, lines = PREFORMATTED, preformatted.group(2).split(), []
                elif preformatted_code:
                    self._append_block(block, params, lines)
                    block, params, lines = PREFORMATTED_CODE, preformatted_code.group(2).split(), []
                elif unordered_list:
                    if block is UNORDERED_LIST:
                        params.append(len(unordered_list.group(1)))
                        lines.append(unordered_list.group(2))
                    else:
                        self._append_block(block, params, lines)
                        block, params, lines = UNORDERED_LIST, [len(unordered_list.group(1))], [unordered_list.group(2)]
                else:
                    if block:
                        self._append_block(block, params, lines)
                        block, params, lines = None, None, []
                    if line:
                        lines.append(line)
                    else:
                        if lines:
                            self.blocks.append((block, params, lines))
                            lines = []
        self._append_block(block, params, lines)
        #from pprint import pprint
        #pprint(self.blocks)

    def _append_block(self, block, params, lines):
        if block or lines:
            self.blocks.append((block, params, lines))

    def to_xhtml(self, fragment=True):
        out = []
        for i, (block, params, lines) in enumerate(self.blocks):
            if block is None:
                line = " ".join(lines)
                out.append("<p>")
                for char, entity in entities:
                    line = line.replace(char, entity)
                for pattern, replacer in elements:
                    line = pattern.sub(replacer, line)
                out.append(line)
                out.append("</p>")
            elif block is HEADING:
                out.append("<h{0}>{1}</h{0}>".format(params, "".join(lines)))
            elif block is HORIZONTAL_RULE:
                out.append("<hr />")
            elif block in (PREFORMATTED, PREFORMATTED_CODE):
                if params:
                    out.append('<pre class="{0}">'.format(" ".join(params)))
                else:
                    out.append('<pre>')
                if block is PREFORMATTED_CODE:
                    out.append('<code>')
                for line in lines:
                    for char, entity in entities:
                        line = line.replace(char, entity)
                    out.append(line)
                if block is PREFORMATTED_CODE:
                    out.append('</code>')
                out.append('</pre>')
            elif block in (ORDERED_LIST, UNORDERED_LIST):
                tag = {
                    ORDERED_LIST: ("<ol>", "</ol>"),
                    UNORDERED_LIST: ("<ul>", "</ul>"),
                }[block]
                level = 0
                for i, line in enumerate(lines):
                    while level > params[i]:
                        out.append(tag[1])
                        level -= 1
                    while level < params[i]:
                        out.append(tag[0])
                        level += 1
                    out.append('<li>')
                    for char, entity in entities:
                        line = line.replace(char, entity)
                    for pattern, replacer in elements:
                        line = pattern.sub(replacer, line)
                    out.append(line)
                    out.append('</li>')
                out.append(tag[1] * level)
        if fragment:
            return "".join(out)
        else:
            return "<html xmlns=\"http://www.w3.org/1999/xhtml\"><head><style type=\"text/css\">{0}</style></head><body>{1}</body></html>".format(
                """""",
                "".join(out)
            )

def to_xhtml(markup, fragment=True):
    out = Document(markup).to_xhtml(fragment)
    #print(out)
    return out

def __test__():
    import json
    import os
    test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "test")
    for file_name in os.listdir(test_dir):
        file_name = os.path.join(test_dir, file_name)
        if os.path.isfile(file_name):
            print(file_name)
            file = open(file_name)
            for line in file:
                line = line.strip()
                values = map(json.loads, line.split("\t"))
                print("    " + " -> ".join(map(json.dumps, values)))
                if values:
                    actual = Document(values[0]).to_xhtml()
                    try:
                        assert actual == values[1]
                    except AssertionError:
                        raise AssertionError("Processing {0} resulted in {1} instead of expected {2}".format(
                            json.dumps(values[0]), json.dumps(actual), json.dumps(values[1])
                        ))
            file.close()

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if args:
        for arg in args:
            file = open(arg)
            print(to_xhtml(file.read(), fragment=False))
            file.close()
    else:
        __test__()
