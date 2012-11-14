#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        self._bits = []
        self.stack = []

    def __str__(self):
        return "".join(self._bits)

    def __repr__(self):
        return str(self)

    def write(self, text):
        self._bits.extend(HTML.entities(text))

    def start_tag(self, tag, attributes=None, void=False):
        if attributes:
            self._bits.append("<{0} {1}>".format(
                tag,
                " ".join(
                    '{0}="{1}"'.format(key, HTML.entities(value))
                    for key, value in attributes.items()
                )
            ))
        else:
            self._bits.append("<{0}>".format(tag))
        if not void:
            self.stack.append(tag)

    def end_tag(self, tag):
        if tag not in self.stack:
            raise ValueError("End tag </{0}> should have corresponding start tag <{0}>".format(tag))
        while True:
            t = self.stack.pop()
            self._bits.append("</{0}>".format(t))
            if t == tag:
                break

    def close(self):
        while self.stack:
            t = self.stack.pop()
            self._bits.append("</{0}>".format(t))
