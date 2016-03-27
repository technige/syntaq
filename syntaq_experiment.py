
from unicodedata import category

### START OF EXPERIMENT ###


NEWLINE_CHARS = u"\u000A\u000B\u000C\u000D\u0085\u2028\u2029"


class Token(object):

    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.source)

    def __str__(self):
        return self.source

    def __len__(self):
        return len(self.source)


class WhitespaceToken(Token):

    pass


class NewlineToken(Token):

    pass


class WordToken(Token):

    pass


class SymbolToken(Token):

    pass


def tokens(source):
    p = 0
    while p < len(source):
        ch = source[p]
        cat = category(ch)
        if ch in NEWLINE_CHARS:
            yield NewlineToken(source[p])
            p += 1
        elif cat[0] in "CZ":
            q = p + 1
            while q < len(source) and category(source[q])[0] in "CZ":
                q += 1
            yield WhitespaceToken(source[p:q])
            p = q
        elif cat[0] in "LN":
            q = p + 1
            while q < len(source) and category(source[q])[0] in "LN":
                q += 1
            yield WordToken(source[p:q])
            p = q
        else:
            q = p + 1
            while q < len(source) and source[q] == ch:
                q += 1
            yield SymbolToken(source[p:q])
            p = q


class Line(object):

    def __init__(self):
        self.tokens = []

    def __repr__(self):
        return "<Line %s>" % "/".join(repr(token.source) for token in self.tokens)

    def __bool__(self):
        num_tokens = len(self.tokens)
        if num_tokens == 0:
            return False
        elif num_tokens == 1 and self.ends_with_newline():
            return False
        else:
            return True

    def __nonzero__(self):
        return self.__bool__()

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)

    def append(self, token):
        self.tokens.append(token)

    def pop(self, index):
        return self.tokens.pop(index)

    def dedent(self):
        t = list(self.tokens)
        while t and isinstance(t[0], WhitespaceToken):
            t.pop(0)
        line = Line()
        line.tokens = t
        return line

    def ends_with_newline(self):
        return isinstance(self.tokens[-1], NewlineToken)

    def first_token_starts_with(self, s):
        return self.tokens and self.tokens[0].source.startswith(s)

    def is_list_item(self, context):
        num_tokens = len(self.tokens) - 1
        i = 0
        while i < num_tokens and isinstance(self.tokens[i], WhitespaceToken):
            i += 1
        if i >= num_tokens:
            return False
        first_non_whitespace_token = self.tokens[i]
        if isinstance(context, List) or not first_non_whitespace_token.startswith("**"):
            return first_non_whitespace_token[0] in "#*"
        else:
            return False


def lines(tokens):
    line = Line()
    for token in tokens:
        line.append(token)
        if line.ends_with_newline():
            yield line
            line = Line()
    if line:
        yield line


class Block2(object):

    pass


class HeadingBlock(Block2):

    def __init__(self, line):
        assert line.first_token_starts_with("=")
        self.level = len(line.pop(0))
        while line and (line.ends_with_newline() or line[-1].startswith("=")):
            line.pop(-1)
        self.line = line


class HorizontalRuleBlock(Block2):

    pass


class List(Block2):

    @classmethod
    def signature(cls, line):
        line = line.dedent()
        s = []
        while True:
            t = line.pop(0)
            if t.source[0] in "#*":
                s.append(t.source)
            else:
                break
        return "".join(s)

    pass


class LiteralBlock(Block2):

    def __init__(self, first_line):
        assert first_line.first_token_starts_with('```')
        self.metadata = "".join(token.source for token in first_line[1:])
        self.lines = []

    def append(self, line):
        self.lines.append(line)

    def text(self):
        # TODO: escaped chars
        s = []
        for line in self.lines:
            for token in line:
                s.append(token.source)
        return "".join(s)


class Paragraph(Block2):

    def __init__(self):
        self.lines = []

    def append(self, line):
        self.lines.append(line)


class Quotation(Block2):

    def __init__(self, first_line):
        assert first_line.first_token_starts_with('"""')
        self.metadata = "".join(token.source for token in first_line[1:])
        self.lines = []

    def append(self, line):
        self.lines.append(line)


class Table(Block2):

    pass


def blocks(lines):
    block = Paragraph()
    for line in lines:
        if isinstance(block, LiteralBlock):
            if line.first_token_starts_with('```'):
                yield block
                block = Paragraph()
            else:
                block.append(line)
        elif isinstance(block, Quotation):
            if line.first_token_starts_with('"""'):
                yield block
                block = Paragraph()
            else:
                block.append(line)
        elif line.first_token_starts_with('='):
            # TODO: title capture
            yield block
            yield HeadingBlock(line)
            block = Paragraph()
        elif line.first_token_starts_with('----'):
            yield block
            yield HorizontalRuleBlock()
            block = Paragraph()
        elif line.first_token_starts_with('```'):
            yield block
            block = LiteralBlock(line)
        elif line.first_token_starts_with('"""'):
            yield block
            block = Quotation(line)
        elif line.first_token_starts_with('|'):
            yield block
            block = Table(line)
        elif line.is_list_item(block):
            if isinstance(block, List) and block.is_compatible(line):
                block.append(line)
            else:
                yield block
                block = List(line)
        else:
            if not isinstance(block, Paragraph):
                yield block
                block = Paragraph()
            if line:
                block.append(line)
            else:
                yield block
                block = Paragraph()
    yield block


### END OF EXPERIMENT ###

