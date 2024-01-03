# High level function that takes input source text and turns it into tokens.
# This is a natural place to use some kind of generator function.
class Token:
    def __init__(self, type, value, lineno, index, end):
        self.value = value
        self.index = index
        self.end = end
        self.type = type
        self.lineno = lineno

    def __repr__(self):
        return f"Token(type='{self.type}', value='{self.value}', lineno={self.lineno}, index={self.index}, end={self.end})"


def tokenize(text):
    ...
    pos = 0
    end = 0
    index = 0
    lineno = 2

    while pos < len(text) - 1:

        value = ""
        type = ""
        if text[pos] == "_" or text[pos].isalpha():
            index = pos
            value += text[pos]
            pos += 1
            while text[pos].isalnum() or text[pos] == '_':
                value += text[pos]  
                pos += 1
            end = pos

            if value == 'var':
                type = 'VAR'
            elif value == 'const':
                type = 'CONST'
            elif value == 'if':
                type = 'IF'
            elif value == 'while':
                type = 'WHILE'
            elif value == 'break':
                type = 'BREAK'
            elif value == 'continue':
                type = 'CONTINUE'
            elif value == 'print':
                type = 'PRINT'
            elif value == 'else':
                type = 'ELSE'
            elif value == 'true':
                type = 'TRUE'
            elif value == 'false':
                type = 'FALSE'
            else:
                type = 'NAME'


        elif text[pos].isdigit() or text[pos] == '.':
            index = pos
            while text[pos].isdigit():
                value += text[pos]
                pos += 1

            if text[pos] == '.':
                type = 'FLOAT'
                value += text[pos]
                pos += 1

            while text[pos].isdigit():
                value += text[pos]
                pos += 1

            end = pos

            if not type:
                type = 'INTEGER'
        elif text[pos] == '+':
            index = pos
            pos += 1
            end = pos
            value = '+'
            type = 'PLUS'

        elif text[pos] == '-':
            index = pos
            pos += 1
            end = pos
            value = '-'
            type = 'MINUS'

        elif text[pos] == '*':
            index = pos
            pos += 1
            end = pos
            value = '*'
            type = 'TIMES'

        elif text[pos] == '/':
            if text[pos+1] == '/':
                while text[pos] != '\n':
                    pos += 1
                pos += 1
            elif text[pos+1] == '*':
                pos += 2
                while text[pos] != '*' and text[pos+1] != '/':
                    pos += 1
                pos += 2

            else:
                index = pos
                pos += 1
                end = pos
                value = '/'
                type = 'DIVIDE'

        elif text[pos] == '<':
            index = pos
            if text[pos+1] == '=':
                type = 'LE'
                value = '<='
                pos += 2
            else:
                type = 'LT'
                value = '<'
                pos += 1

            end = pos

        elif text[pos] == '>':
            index = pos
            if text[pos+1] == '=':
                type = 'GE'
                value = '>='
                pos += 2
            else:
                type = 'GT'
                value = '>'
                pos += 1

            end = pos

        elif text[pos] == '=':
            index = pos
            if text[pos+1] == '=':
                type = 'EQ'
                value = '=='
                pos += 2
            else:
                type = 'ASSIGN'
                value = '='
                pos += 1

            end = pos

        elif text[pos] == '!':
            index = pos
            if text[pos+1] == '=':
                type = 'NE'
                value = '!='
                pos += 2
            else:
                type = 'LNOT'
                value = '!'
                pos += 1

            end = pos


        elif text[pos] == '|' and text[pos+1] == '|':
            index = pos
            type = 'LOR'
            value = '||'
            pos += 2
            end = pos

        elif text[pos] == '&' and text[pos+1] == '&':
            index = pos
            type = 'LAND'
            value = '&&'
            pos += 2
            end = pos


        elif text[pos] == ';':
            index = pos
            type = 'SEMI'
            value = ';'
            pos += 1
            end = pos

        elif text[pos] == '(':
            index = pos
            type = 'LPAREN'
            value = '('
            pos += 1
            end = pos

        elif text[pos] == ')':
            index = pos
            type = 'RPAREN'
            value = ')'
            pos += 1
            end = pos


        elif text[pos] == '{':
            index = pos
            type = 'LBRACE'
            value = '{'
            pos += 1
            end = pos

        elif text[pos] == '}':
            index = pos
            type = 'RBRACE'
            value = '}'
            pos += 1
            end = pos

        elif text[pos] == "'":
            index = pos
            type = 'CHAR'
            value += text[pos]
            pos += 1
            while text[pos] != "'":
                value += text[pos]
                pos += 1

            value += text[pos]
            pos += 1
            end = pos

        elif text[pos] == '\n':
            while text[pos].isspace():
                pos += 1

            lineno += 1

        elif text[pos].isspace():
            while text[pos].isspace() and text[pos] != '\n':
                pos += 1

        
        elif text[pos] == '%' and text[pos+1] == '%':
            while text[pos] != '\n':
                pos += 1
            pos += 1
            text = text[pos:]
            pos = 0

        if type:
            tok = Token(type, value, lineno, index, end)
            yield tok

                
