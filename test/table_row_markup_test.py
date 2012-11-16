#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from syntaq import TableRowMarkup


class TableRowMarkupTester(unittest.TestCase):

    def test_single_cell(self):
        line = TableRowMarkup("|foo")
        assert line.to_html() == "<tr><td>foo</td></tr>"

    def test_single_cell_with_trailing_pipe(self):
        line = TableRowMarkup("|foo|")
        assert line.to_html() == "<tr><td>foo</td></tr>"

    def test_single_cell_with_trailing_pipe_and_whitespace(self):
        line = TableRowMarkup("|foo| ")
        assert line.to_html() == "<tr><td>foo</td></tr>"

    def test_multiple_cells(self):
        line = TableRowMarkup("|foo|bar")
        assert line.to_html() == "<tr><td>foo</td><td>bar</td></tr>"

    def test_multiple_cells_with_trailing_pipe(self):
        line = TableRowMarkup("|foo|bar|")
        assert line.to_html() == "<tr><td>foo</td><td>bar</td></tr>"

    def test_multiple_cells_with_trailing_pipe_and_whitespace(self):
        line = TableRowMarkup("|foo|bar| ")
        assert line.to_html() == "<tr><td>foo</td><td>bar</td></tr>"

    def test_empty_cell_at_start(self):
        line = TableRowMarkup("||bar|")
        assert line.to_html() == "<tr><td></td><td>bar</td></tr>"

    def test_empty_cell_at_end(self):
        line = TableRowMarkup("|foo||")
        assert line.to_html() == "<tr><td>foo</td><td></td></tr>"

    def test_cell_with_pipe_in_name(self):
        line = TableRowMarkup("|foo ~| bar|baz|")
        assert line.to_html() == "<tr><td>foo | bar</td><td>baz</td></tr>"

    def test_cell_with_tilde_at_end_of_name(self):
        line = TableRowMarkup("|foo~~|bar|baz|")
        assert line.to_html() == "<tr><td>foo~</td><td>bar</td><td>baz</td></tr>"

    def test_cell_with_tilde_pipe_in_name(self):
        line = TableRowMarkup("|foo~~~|bar|baz|")
        assert line.to_html() == "<tr><td>foo~|bar</td><td>baz</td></tr>"

    def test_cell_with_double_tilde_at_end_of_name(self):
        line = TableRowMarkup("|foo~~~~|bar|baz|")
        assert line.to_html() == "<tr><td>foo~~</td><td>bar</td><td>baz</td></tr>"

    def test_cells_with_trailing_tilde(self):
        line = TableRowMarkup("|foo|bar~")
        assert line.to_html() == "<tr><td>foo</td><td>bar~</td></tr>"

    def test_header_cell(self):
        line = TableRowMarkup("|=foo")
        assert line.to_html() == "<tr><th>foo</th></tr>"

    def test_header_cell_with_trailing_pipe(self):
        line = TableRowMarkup("|=foo|")
        assert line.to_html() == "<tr><th>foo</th></tr>"

    def test_multiple_header_cells(self):
        line = TableRowMarkup("|=foo|=bar|")
        assert line.to_html() == "<tr><th>foo</th><th>bar</th></tr>"

    def test_mixed_cell_types(self):
        line = TableRowMarkup("|=foo|bar|=baz|qux|")
        assert line.to_html() == "<tr><th>foo</th><td>bar</td><th>baz</th><td>qux</td></tr>"

    def test_left_aligned_cell(self):
        line = TableRowMarkup("|foo |")
        assert line.to_html() == '<tr><td style="text-align:left">foo</td></tr>'

    def test_right_aligned_cell(self):
        line = TableRowMarkup("| foo|")
        assert line.to_html() == '<tr><td style="text-align:right">foo</td></tr>'

    def test_center_aligned_cell(self):
        line = TableRowMarkup("| foo |")
        assert line.to_html() == '<tr><td style="text-align:center">foo</td></tr>'

    def test_left_aligned_header_cell(self):
        line = TableRowMarkup("|=foo |")
        assert line.to_html() == '<tr><th style="text-align:left">foo</th></tr>'

    def test_right_aligned_header_cell(self):
        line = TableRowMarkup("|= foo|")
        assert line.to_html() == '<tr><th style="text-align:right">foo</th></tr>'

    def test_center_aligned_header_cell(self):
        line = TableRowMarkup("|= foo |")
        assert line.to_html() == '<tr><th style="text-align:center">foo</th></tr>'

    def test_cell_with_entity(self):
        line = TableRowMarkup("|foo & bar|")
        assert line.to_html() == '<tr><td>foo &amp; bar</td></tr>'

    def test_cell_with_markup(self):
        line = TableRowMarkup("|foo **bar**|")
        assert line.to_html() == '<tr><td>foo <strong>bar</strong></td></tr>'

    def test_cell_with_link_and_description(self):
        line = TableRowMarkup("|[[foo|bar]]|")
        assert line.to_html() == '<tr><td><a href="foo">bar</a></td></tr>'

    def test_cell_with_code(self):
        line = TableRowMarkup("|``foo|bar``|")
        assert line.to_html() == '<tr><td><code>foo|bar</code></td></tr>'

    def test_cell_with_preformatted_content(self):
        line = TableRowMarkup("|{{{foo|bar}}}|")
        assert line.to_html() == '<tr><td>foo|bar</td></tr>'

    def test_cell_with_image_and_alt(self):
        line = TableRowMarkup("|{{foo.jpg|bar}}|")
        assert line.to_html() == '<tr><td><img src="foo.jpg" alt="bar"></td></tr>'

    def test_cell_with_link_and_image(self):
        line = TableRowMarkup("|[[foo|{{bar.jpg|baz}}]]|")
        assert line.to_html() == '<tr><td><a href="foo"><img src="bar.jpg" alt="baz"></a></td></tr>'

    def test_cell_with_unclosed_brackets(self):
        line = TableRowMarkup("|[[foo|{{bar.jpg|baz|")
        assert line.to_html() == '<tr><td><a href="foo"><img src="bar.jpg" alt="baz"></a></td></tr>'

    def test_cells_with_multiple_brackets(self):
        line = TableRowMarkup("|[[foo]]|[[foo~|bar]]|[[foo|bar]]|``foo|bar``|{{{foo|bar}}}|{{foo.jpg|bar}}|[[foo|{{bar.jpg|baz}}]]|")
        assert line.to_html() == '<tr><td><a href="foo">foo</a></td><td><a href="foo~|bar">foo~|bar</a></td><td>' \
                                 '<a href="foo">bar</a></td><td><code>foo|bar</code></td><td>foo|bar</td><td>' \
                                 '<img src="foo.jpg" alt="bar"></td><td><a href="foo"><img src="bar.jpg" alt="baz">' \
                                 '</a></td></tr>'


if __name__ == "__main__":
    unittest.main()
