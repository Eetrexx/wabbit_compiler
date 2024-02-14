# High level function that takes input source text and turns it into tokens.
# This is a natural place to use some kind of generator function.

from sly import Lexer


class CalcLexer(Lexer):

    tokens = { CONST, VAR, PRINT, BREAK, CONTINUE, IF, ELSE, WHILE, TRUE, FALSE, NAME, INTEGER, FLOAT, CHAR, PLUS, MINUS, TIMES, DIVIDE, LT, LE, GT, GE, EQ, NE, LAND, LOR, LNOT, ASSIGN, SEMI, LPAREN, RPAREN, LBRACE, RBRACE }

    ignore = ' \t'
    ignore_comment = r'//[^\n]*'
    ignore_comment_block = r"/[*]([^*]|([*][^/]))*[*]/"
    ignore_start_file = r'%%.*'

    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    LAND    = r'&&'
    LOR     = r'\|\|'
    LNOT    = r'!'
    SEMI    = r';'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LBRACE  = r'\{'
    RBRACE  = r'\}'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    NAME['const'] = CONST
    NAME['var'] = VAR
    NAME['print'] = PRINT
    NAME['break'] = BREAK
    NAME['continue'] = CONTINUE
    NAME['if'] = IF
    NAME['else'] = ELSE
    NAME['while'] = WHILE
    NAME['true'] = TRUE
    NAME['false'] = FALSE



    FLOAT = r'(\d+\.\d+|\d+\.|\.\d+)'
    INTEGER = r'\d+'
    
    CHAR = r'\'(.|\\n|\\x[a-fA-F0-9][a-fA-F0-9])\''

        
    @_(r"/[*]([^*]|([*][^/]))*[*]/")
    def ignore_comment_block(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


def tokenize(text):
    lexer = CalcLexer() 

    for tok in lexer.tokenize(text):
        yield tok
