#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import string


HEADING = re.compile(r"^(={1,6})\s*(.*[^=\s])\s*=*")
HORIZONTAL_RULE = re.compile(r"^(-{4})")
ORDERED_LIST = re.compile(r"^(#+)\s*(.*)")
PREFORMATTED = re.compile(r"^(\{\{\{)\s*([-:\s\w]*)", re.UNICODE)
BLOCK_CODE = re.compile(r"^(```)\s*([-:\s\w]*)", re.UNICODE)
UNORDERED_LIST = re.compile(r"^(\*+)\s*(.*)")

END_OF_PREFORMATTED = re.compile(r"^\s*(\}\}\})")
END_OF_BLOCK_CODE = re.compile(r"^\s*(```)")


class HTML(object):

    @staticmethod
    def entities(text):
        chars = list(text)
        for i, ch in enumerate(chars):
            if ch == "&":
                chars[i] = "&amp;"
            elif ch == "'":
                chars[i] = "&apos;"
            elif ch == "\"":
                chars[i] = "&quot;"
            elif ch == "<":
                chars[i] = "&lt;"
            elif ch == ">":
                chars[i] = "&gt;"
        return "".join(chars)


class HTMLOutputStream(object):

    def __init__(self):
        self.tokens = []
        self.stack = []

    def __str__(self):
        return "".join(self.tokens)

    def __repr__(self):
        return str(self)

    def write_html(self, html):
        self.tokens.append(html)

    def write_text(self, text):
        self.tokens.extend(HTML.entities(text))

    def tag(self, tag, attributes=None):
        if attributes:
            self.tokens.append("<{0} {1}>".format(
                tag,
                " ".join(
                    '{0}="{1}"'.format(key, HTML.entities(value))
                    for key, value in attributes.items()
                    if value is not None
                )
            ))
        else:
            self.tokens.append("<{0}>".format(tag))

    def start_tag(self, tag, attributes=None, void=False):
        self.tag(tag, attributes)
        if not void:
            self.stack.append(tag)

    def end_tag(self, tag=None):
        if not self.stack:
            raise ValueError("No tags to close")
        if not tag:
            tag = self.stack[-1]
        if tag not in self.stack:
            raise ValueError("End tag </{0}> should have corresponding start tag <{0}>".format(tag))
        while True:
            t = self.stack.pop()
            self.tokens.append("</{0}>".format(t))
            if t == tag:
                break

    def element(self, tag, attributes=None, text=None, html=None):
        if text and html:
            raise ValueError("Cannot specify both text and html content")
        self.start_tag(tag, attributes)
        if text:
            self.write_text(text)
        if html:
            self.write_html(html)
        self.end_tag()

    def close(self):
        while self.stack:
            t = self.stack.pop()
            self.tokens.append("</{0}>".format(t))


class Tokeniser(object):

    def __init__(self, escape, *markers):
        self.escape = escape
        self.markers = [self.escape]
        self.markers.extend(markers)
        self.marker_chars = list(set(marker[0] for marker in self.markers))

    def tokenise(self, markup):
        self.tokens = []
        p, q = 0, 0
        while q < len(markup):
            if markup[q] in self.marker_chars:
                start = q + len(self.escape) if markup[q] == self.escape else q
                for seq in self.markers:
                    end = start + len(seq)
                    if markup[start:end] == seq:
                        if q > p:
                            yield markup[p:q]
                        yield markup[q:end]
                        p, q = end, end
                        break
                else:
                    q += 1
            else:
                q += 1
        if q > p:
            yield markup[p:q]


class InlineMarkup(object):

    def __init__(self, markup=None):
        tokeniser = Tokeniser("~",
            "http://", "https://", "ftp://", "mailto:",
            "\\\\", "{{{", "}}}", "{{", "}}", "``", '""',
            "**", "//", "^^", ",,", "[[", "]]", "|"
        )
        self.tokens = list(tokeniser.tokenise(markup))

    def to_html(self):

        def image(out, markup):
            src, alt = markup.partition("|")[0::2]
            out.tag("img", {"src": src, "alt": alt or None})

        toggle_tokens = {
            "//": "em",
            '""': "q",
            "**": "strong",
            ",,": "sub",
            "^^": "sup",
        }
        bracket_tokens = {
            "``" : ("``", lambda out, markup: out.element("code", text=markup)),
            "{{" : ("}}", image),
            "{{{": ("}}}", lambda out, markup: out.write_text(markup)),
        }

        out = HTMLOutputStream()
        tokens = self.tokens[:]
        while tokens:
            token = tokens.pop(0)
            if token[0] == "~":
                out.write_text(token[1:])
            elif token == "\\\\":
                out.tag("br")
            elif token in toggle_tokens:
                tag = toggle_tokens[token]
                if tag in out.stack:
                    out.end_tag(tag)
                else:
                    out.start_tag(tag)
            elif token in bracket_tokens:
                end_token, writer = bracket_tokens[token]
                markup = []
                while tokens:
                    token = tokens.pop(0)
                    if token == end_token:
                        break
                    else:
                        markup.append(token)
                writer(out, "".join(markup))
            elif token == "[[":
                href = []
                while tokens:
                    token = tokens.pop(0)
                    if token in ("|", "]]"):
                        break
                    else:
                        href.append(token)
                href = "".join(href)
                out.start_tag("a", {"href": href})
                if token != "|":
                    out.write_text(href)
                    out.end_tag("a")
            elif token == "]]":
                try:
                    out.end_tag("a")
                except ValueError:
                    out.write_text(token)
            else:
                out.write_text(token)
        out.close()
        return str(out)


class TableRowMarkup(object):

    def __init__(self, markup):
        assert markup.startswith("|")
        markup = markup.strip()
        if markup.endswith("|"):
            self.cells = markup[1:-1].split("|")
        else:
            self.cells = markup[1:].split("|")
        deleted_cells = []
        for i, cell in enumerate(self.cells):
            if cell.endswith("~"):
                tildes = 1
                while cell.endswith("~" * tildes):
                    tildes += 1
                escaped = tildes % 2 == 1
                if not escaped:
                    try:
                        self.cells[i] += "|" + self.cells[i + 1]
                        deleted_cells.append(i + 1)
                    except IndexError:
                        pass
        for i in deleted_cells:
            del self.cells[i]

    def to_html(self):
        out = HTMLOutputStream()
        out.start_tag("tr")
        for cell in self.cells:
            if cell.startswith("="):
                tag = "th"
                content = cell[1:]
            else:
                tag = "td"
                content = cell
            align = None
            if content:
                left_padded = content[0] in string.whitespace
                right_padded = content[-1] in string.whitespace
                if left_padded and right_padded:
                    align = "center"
                elif right_padded:
                    align = "left"
                elif left_padded:
                    align = "right"
            if align:
                content = content.strip()
                out.element(tag, {"style": "align:" + align}, html=InlineMarkup(content).to_html())
            else:
                out.element(tag, html=InlineMarkup(content).to_html())
        out.close()
        print(str(out))
        return str(out)


class Markup(object):

    def __init__(self, markup):
        self.blocks = []
        block, params, lines = None, None, []
        for line in markup.splitlines(True):
            if block is PREFORMATTED:
                at_end = END_OF_PREFORMATTED.match(line)
                if at_end:
                    self._append_block(block, params, lines)
                    block, params, lines = None, None, []
                else:
                    lines.append(line)
            elif block is BLOCK_CODE:
                at_end = END_OF_BLOCK_CODE.match(line)
                if at_end:
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
                block_code = BLOCK_CODE.match(line)
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
                elif block_code:
                    self._append_block(block, params, lines)
                    block, params, lines = BLOCK_CODE, block_code.group(2).split(), []
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

    def to_html(self):
        out = HTMLOutputStream()
        for i, (block, params, lines) in enumerate(self.blocks):
            if block is None:
                out.element("p", html=InlineMarkup(" ".join(lines)).to_html())
            elif block is HEADING:
                out.element("h" + str(params), text="".join(lines))
            elif block is HORIZONTAL_RULE:
                out.tag("hr")
            elif block in (PREFORMATTED, BLOCK_CODE):
                if params:
                    out.start_tag("pre", {"class": " ".join(params)})
                else:
                    out.start_tag("pre")
                if block is BLOCK_CODE:
                    out.start_tag("code")
                for line in lines:
                    out.write_text(line)
                out.end_tag("pre")
            elif block in (ORDERED_LIST, UNORDERED_LIST):
                if block is ORDERED_LIST:
                    tag = "ol"
                else:
                    tag = "ul"
                level = 0
                for i, line in enumerate(lines):
                    while level > params[i]:
                        out.end_tag(tag)
                        level -= 1
                    while level < params[i]:
                        out.start_tag(tag)
                        level += 1
                    out.element("li", html=InlineMarkup(line).to_html())
                for i in range(level):
                    out.end_tag(tag)
        return str(out)

def to_html(markup):
    out = Markup(markup).to_html()
    #print(out)
    return out

def __test__():
    import json
    import os
    test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "test")
    for file_name in os.listdir(test_dir):
        file_name = os.path.join(test_dir, file_name)
        if os.path.isfile(file_name) and file_name.endswith(".tsv"):
            print(file_name)
            file = open(file_name)
            for line in file:
                line = line.strip()
                values = map(json.loads, line.split("\t"))
                print("    " + " -> ".join(map(json.dumps, values)))
                if values:
                    actual = Markup(values[0]).to_html()
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
            print(to_html(file.read()))
            file.close()
    else:
        __test__()
