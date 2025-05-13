from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter


class MyFormatter(Formatter):

    def __init__(self, tk_panel):
        Formatter.__init__(self)
        self.tk_panel = tk_panel

        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:
            token_name = str(token)
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color']:
                value = '#%s' % style['color']
                tk_panel.tag_configure(token_name, foreground=value)
                print(token_name, value)
#            if style['bold']:
#                start += '<b>'
#            if style['italic']:
#                start += '<i>'
#            if style['underline']:
#                start += '<u>'
            self.styles[token] = token_name


    def format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here
        lastval = ''
        lasttype = None

        for ttype, value in tokensource:
            # if the token type doesn't exist in the stylemap
            # we try it with the parent of the token type
            # eg: parent of Token.Literal.String.Double is
            # Token.Literal.String
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                # the current token type is the same of the last
                # iteration. cache it
                lastval += value
            else:
                # not the same token as last iteration, but we
                # have some data in the buffer. wrap it with the
                # defined style and write it to the output file
                if lastval:
                    token = self.styles[lasttype]
#                    before = self.tk_panel.index('end')
                    self.tk_panel.insert('end', lastval, (token,))
#                    self.tk_panel.tag_add(token, before, 'end')
                # set lastval/lasttype to current values
                lastval = value
                lasttype = ttype

        # if something is left in the buffer, write it to the
        # output file, then close the opened <pre> tag
        if lastval:
            token = self.styles[lasttype]
 #           before = self.tk_panel.index('end')
            self.tk_panel.insert('end', lastval, (token,))
 #           self.tk_panel.tag_add(token, before, 'end')


class TkFormatter:

    def __init__(self, tk_panel):
        self.lexer = get_lexer_by_name("cpp")
        self.formatter = MyFormatter(tk_panel)


    def insert(self, line):
        line = highlight(line, self.lexer, self.formatter)
        print(line)

