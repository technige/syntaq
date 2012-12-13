#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011-2012 Nigel Small
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


import re
import string

__author__    = "Nigel Small <nigel@nigelsmall.com>"
__copyright__ = "Copyright 2012 Nigel Small"
__license__   = "Apache License, Version 2.0"
__package__   = "syntaq"
__version__   = "0.8"


SYNTAQ_CSS = """\
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, font, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td {
	margin: 0;
	padding: 0;
	border: 0;
	outline: 0;
	font-weight: inherit;
	font-style: inherit;
	font-size: 100%;
    font-family: inherit;
	vertical-align: baseline;
}
/* remember to define focus styles! */
:focus {
	outline: 0;
}
html {
    font-family: "Droid Sans", "Lucida Sans", "Trebuchet", sans-serif;
    /* font-family: "Droid Serif", "Lucida Bright", "Georgia", serif; */
    font-size: 12pt;
	line-height: 150%;
    background-color: #FBFBF7;
    margin: 20px;
}
body {
    font-family: "Droid Sans", "Lucida Sans", "Trebuchet", sans-serif;
    /* font-family: "Droid Serif", "Lucida Bright", "Georgia", serif; */
    font-size: 12pt;
	line-height: 150%;
    background-color: transparent;
    color: #141410;
}

/* Headings */
h1 { font-weight: bold; font-size: 200%; margin: .25em 0 .5em 0; }
h2 { font-weight: bold; font-size: 150%; margin: .75em 0 .5em 0; padding-top: .75em; border-top: 1px solid #CCC; }
h3 { font-weight: bold; font-size: 125%; margin: .75em 0 .5em 0; }
h4 { font-weight: bold; font-size: 100%; margin: .75em 0 .5em 0; }
h5 { font-weight: bold; font-size: 90%; margin: .75em 0 .5em 0; }
h6 { font-weight: bold; font-size: 80%; margin: .75em 0 .5em 0; }

code, pre, tt {
    font-family: "Droid Sans Mono", "Lucida Sans Typewriter", "Andale Mono", monospace;
    line-height: 150%;
}

ol {
	list-style: decimal inside;
	margin-left: 1em;
}
ul {
	list-style: disc inside;
	margin-left: 1em;
}

/* Tables */
/* tables still need 'cellspacing="0"' in the markup */
table {
    border-collapse: collapse;
    margin: .75em 0;
	border-spacing: 0;
}
caption, th, td {
	text-align: left;
	font-weight: normal;
    border: 1px solid #CCC;
    padding: .25em .5em;
}

/* Quotations */
blockquote:before, blockquote:after,
q:before, q:after {
	content: "";
}
blockquote, q {
	quotes: "" "";
}

p { margin: .75em 0; }
em { font-style: italic; }
strong { font-weight: bold; }
sup { font-size: .7em; position: relative; top: -.4em; }
sub { font-size: .7em; position: relative; bottom: -.4em; }
code {background-color: #E7E7E7;}

a {
    color: #0087BD;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
.hashtag {
    color: #009F6B;
}

/* Preformatted and code blocks */
pre {
    display: block;
    background-color: #E7E7E7;
    color: #222;
    border: 1px solid #CCC;
    margin: .75em 0;
    padding: .5em .5em .5em .75em;
    overflow: auto;
    cursor: text;
}
pre>ol {
    list-style: decimal outside;
	margin-left: 3em;
	background-color: inherit;
}
pre>ol>li {
    border-left: 1px solid #BBB;
}
pre>ol>li:hover {
    background-color: #D7D7D7;
}
pre>ol>li>code {
    color: #222;
	margin-left: 1em;
	background-color: inherit;
}
"""

DOCUMENT_TEMPLATE="""\
<!doctype html>
<html>
<head><title>{title}</title><style type="text/css">{css}</style>{head}</head>
<body>{body}</body>
</html>
"""

URL = re.compile(r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""")


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

    def __init__(self, processor=None):
        self.tokens = []
        self.stack = []
        self.token_buffer = []
        self.processor = processor or HTML.entities

    def __html__(self):
        return "".join(self.tokens)

    def __repr__(self):
        return self.__html__()

    def _flush(self):
        if self.token_buffer:
            buffer = "".join(self.token_buffer)
            self.tokens.append(self.processor(buffer))
            self.token_buffer = []

    def write_html(self, html):
        self._flush()
        self.tokens.append(html)

    def write_text(self, text, post_process=False):
        if post_process:
            self.token_buffer.extend(text)
        else:
            self._flush()
            self.tokens.extend(HTML.entities(text))

    def tag(self, tag, attributes=None):
        if attributes:
            self.write_html("<{0} {1}>".format(
                tag,
                " ".join(
                    '{0}="{1}"'.format(key, HTML.entities(str(value)))
                    for key, value in attributes.items()
                    if value is not None
                )
            ))
        else:
            self.write_html("<{0}>".format(tag))

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
            self.write_html("</{0}>".format(t))
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
        self._flush()
        while self.stack:
            t = self.stack.pop()
            self.write_html("</{0}>".format(t))


class Partitioner(object):

    def __init__(self, escape, *markers):
        self.escape = escape
        if escape:
            self.markers = [self.escape]
        else:
            self.markers = []
        self.markers.extend(markers)
        self.marker_chars = list(set(marker[0] for marker in self.markers))

    def partition(self, markup):
        self.tokens = []
        p, q = 0, 0
        while q < len(markup):
            if markup[q] in self.marker_chars:
                if self.escape and markup[q] == self.escape:
                    start = q + len(self.escape)
                else:
                    start = q
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
        partitioner = Partitioner("~",
            "http://", "https://", "ftp://", "mailto:",
            '"""', "{{{", "}}}", "<--", "-->",
            "\\\\", "{{", "}}", "``", '""',
            "**", "//", "^^", ",,", "[[", "]]", "|"
        )
        self.tokens = list(partitioner.partition(markup))

    def __html__(self):

        def image(out, markup):
            src, alt = markup.partition("|")[0::2]
            out.tag("img", {"src": src, "alt": alt or None})

        def auto_link(text):
            out = HTMLOutputStream()
            bits = URL.split(text)
            out.write_text(bits[0])
            p = 1
            while p < len(bits):
                url = bits[p]
                out.element("a", {"href": url}, text=url)
                p += 5
                out.write_text(bits[p])
                p += 1
            return out.__html__()

        simple_tokens = {
            "\\\\": "<br>",
            "-->": "&rarr;",
            "<--": "&larr;",
        }
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

        out = HTMLOutputStream(processor=auto_link)
        tokens = self.tokens[:]
        while tokens:
            token = tokens.pop(0)
            if token[0] == "~":
                out.write_text(token[1:])
            elif token in simple_tokens:
                out.write_html(simple_tokens[token])
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
                    elif token[0] == "~":
                        markup.append(token[1:])
                    else:
                        markup.append(token)
                writer(out, "".join(markup))
            elif token == "[[":
                href = []
                while tokens:
                    token = tokens.pop(0)
                    if token in ("|", "]]"):
                        break
                    elif token[0] == "~":
                        href.append(token[1:])
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
                out.write_text(token, post_process=True)
        out.close()
        return out.__html__()


class HeadingMarkup(object):

    def __init__(self, markup):
        if not markup.startswith("="):
            raise ValueError("Heading must start with '='")
        chars = list(markup)
        self.level = 0
        while chars and chars[0] == "=":
            chars.pop(0)
            self.level += 1
        self.text = "".join(chars).strip().rstrip("=").rstrip()
        if self.level > 6:
            self.level = 6

    def __html__(self):
        out = HTMLOutputStream()
        out.element("h" + str(self.level), text=self.text)
        return out.__html__()


class HorizontalRuleMarkup(object):

    def __init__(self, markup):
        if not markup.startswith("----"):
            raise ValueError("Horizontal rule must start with '----'")

    def __html__(self):
        out = HTMLOutputStream()
        out.tag("hr")
        return out.__html__()


class ListItemMarkup(object):

    def __init__(self, markup):
        if not (markup.startswith("#") or markup.startswith("*")):
            raise ValueError("List items must start with either '#' or '*'")
        chars = list(markup)
        self.signature = []
        while chars and chars[0] in ("#", "*"):
            self.signature.append(chars.pop(0))
        self.signature = tuple(self.signature)
        self.level = len(self.signature)
        self.item = InlineMarkup("".join(chars).strip())

    def ordered(self, level):
        return self.signature[level] == "#"

    def list_tag(self, level):
        if self.ordered(level):
            return "ol"
        else:
            return "ul"

    def compatible(self, other):
        m = min(len(self.signature), len(other.signature))
        return self.signature[0:m] == other.signature[0:m]

    def __html__(self):
        out = HTMLOutputStream()
        out.element("li", html=self.item.__html__())
        return out.__html__()


class PreformattedMarkup(object):

    def __init__(self, markup):
        self.text = markup

    def __html__(self):
        out = HTMLOutputStream()
        out.write_text(self.text)
        return out.__html__()


class LineOfCodeMarkup(object):

    def __init__(self, markup):
        self.line = markup

    def __html__(self):
        out = HTMLOutputStream()
        out.start_tag("li")
        out.element("code", text=self.line)
        out.end_tag()
        return out.__html__()


class TableRowMarkup(object):

    def __init__(self, markup):
        if not markup.startswith("|"):
            raise ValueError("Table row must start with '|'")
        bracket_tokens = {
            "``" : "``",
            "[[" : "]]",
            "{{" : "}}",
            "{{{": "}}}",
            }
        partitioner = Partitioner("~", "|", "``", "[[", "]]", "{{", "}}", "{{{", "}}}")
        markup = markup.rstrip()
        if markup.endswith("|"):
            tokens = list(partitioner.partition(markup[:-1]))
        else:
            tokens = list(partitioner.partition(markup))
        self.cells = []
        while tokens:
            token = tokens.pop(0)
            if token == "|":
                self.cells.append([])
            elif token in bracket_tokens:
                end = bracket_tokens[token]
                self.cells[-1].append(token)
                while tokens:
                    token = tokens.pop(0)
                    self.cells[-1].append(token)
                    if token == end:
                        break
            else:
                self.cells[-1].append(token)
        self.cells = ["".join(cell) for cell in self.cells]

    def __html__(self):
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
                out.element(tag, {"style": "text-align:" + align}, html=InlineMarkup(content).__html__())
            else:
                out.element(tag, html=InlineMarkup(content).__html__())
        out.end_tag("tr")
        return out.__html__()


class Block(object):

    def __init__(self, content_type=None, params=None, lines=None):
        self.content_type = content_type
        self.params = params
        self.lines = []
        if lines:
            for line in lines:
                self.append(line)

    def __len__(self):
        return len(self.lines)

    def __nonzero__(self):
        return bool(self.lines)

    def append(self, line):
        if not self.content_type or isinstance(line, self.content_type):
            self.lines.append(line)
        else:
            raise ValueError("Cannot add {0} to block of {1}".format(line.__class__.__name__, self.content_type.__name__))


class Markup(object):

    def __init__(self, markup):
        self.blocks = []
        self.title = None
        title_level = 7
        block = Block()
        for line in markup.splitlines(True):
            if block.content_type is PreformattedMarkup:
                if line.startswith("}}}"):
                    self.append(block)
                    block = Block()
                else:
                    block.lines.append(PreformattedMarkup(line))
            elif block.content_type is LineOfCodeMarkup:
                if line.startswith("```"):
                    self.append(block)
                    block = Block()
                else:
                    block.lines.append(LineOfCodeMarkup(line))
            else:
                line = line.rstrip()
                stripped_line = line.lstrip()
                if line.startswith("="):
                    self.append(block)
                    block = Block()
                    markup = HeadingMarkup(line)
                    self.blocks.append(Block(HeadingMarkup, lines=[markup]))
                    if not self.title or markup.level < title_level:
                        self.title, title_level = markup.text, markup.level
                elif line.startswith("----"):
                    self.append(block)
                    block = Block()
                    self.blocks.append(Block(HorizontalRuleMarkup, lines=[HorizontalRuleMarkup(line)]))
                elif stripped_line.startswith("#") or stripped_line.startswith("*"):
                    markup = ListItemMarkup(stripped_line)
                    if not (block and block.content_type is ListItemMarkup and block.lines[0].compatible(markup)):
                        self.append(block)
                        block = Block(ListItemMarkup)
                    block.lines.append(markup)
                elif line.startswith("{{{"):
                    params = line.lstrip("{").strip().split()
                    self.append(block)
                    block = Block(PreformattedMarkup, params=params)
                elif line.startswith("```"):
                    params = line.lstrip("`").strip().split()
                    self.append(block)
                    block = Block(LineOfCodeMarkup, params=params)
                elif line.startswith("|"):
                    if not block.content_type is TableRowMarkup:
                        self.append(block)
                        block = Block(TableRowMarkup)
                    block.lines.append(TableRowMarkup(line))
                else:
                    if block.content_type is not None:
                        self.append(block)
                        block = Block()
                    if line:
                        block.lines.append(line)
                    else:
                        if block:
                            self.blocks.append(block)
                            block = Block()
        self.append(block)

    def append(self, block):
        if block:
            self.blocks.append(block)

    def __html__(self):
        out = HTMLOutputStream()
        for block in self.blocks:
            if block.content_type is None:
                out.element("p", html=InlineMarkup(" ".join(block.lines)).__html__())
            elif block.content_type in (HeadingMarkup, HorizontalRuleMarkup):
                for line in block.lines:
                    out.write_html(line.__html__())
            elif block.content_type in (LineOfCodeMarkup, PreformattedMarkup):
                if block.params:
                    out.start_tag("pre", {"class": " ".join(block.params)})
                else:
                    out.start_tag("pre")
                if block.content_type is LineOfCodeMarkup:
                    out.start_tag("ol")
                for line in block.lines:
                    out.write_html(line.__html__())
                out.end_tag("pre")
            elif block.content_type is ListItemMarkup:
                level = 0
                for line in block.lines:
                    while level > line.level:
                        out.end_tag()
                        level -= 1
                    while level < line.level:
                        out.start_tag(line.list_tag(level))
                        level += 1
                    out.write_html(line.__html__())
                while level:
                    out.end_tag()
                    level -= 1
            elif block.content_type is TableRowMarkup:
                out.start_tag("table", {"cellspacing": 0})
                for line in block.lines:
                    out.write_html(line.__html__())
                out.end_tag("table")
        return out.__html__()


class StyleSheet(object):

    def __init__(self):
        pass

    def __css__(self):
        return SYNTAQ_CSS


class Document(object):

    def __init__(self, markup):
        self.markup = Markup(markup)

    def __html__(self):
        return DOCUMENT_TEMPLATE.format(
            title=self.markup.title or "",
            css=StyleSheet().__css__(),
            head="",
            body=self.markup.__html__(),
        )


if __name__ == "__main__":
    import codecs
    import sys
    if len(sys.argv) > 1:
        markup = codecs.open(sys.argv[1], "r", "UTF-8").read()
        print(Document(markup).__html__())
