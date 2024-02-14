# Top-level function that runs everything

from sly import Parser
from sly.yacc import SlyLogger
from tokenize import * 
from model import *

class MyLogger(SlyLogger):
    pass

class CalcParser(Parser):

    tokens = CalcLexer.tokens
    f = open("logging.out", "wt")
    log = MyLogger(f) 

    precedence = (
            ('left', LOR),
            ('left', LAND),
            ('nonassoc', LT, LE, GT, GE, EQ, NE),
            ('left', PLUS, MINUS),
            ('left', TIMES, DIVIDE),
            ('right', UPLUS, UMINUS, LNOT),
    )

    @_('{ statement }')
    def statements(self, p):
       return p.statement 

    @_('print_statement')
    def statement(self, p):
        return p.print_statement

    @_('assignment_statement')
    def statement(self, p):
        return p.assignment_statement
    
    @_('variable_definition')
    def statement(self, p):
        return p.variable_definition

    @_('const_definition')
    def statement(self, p):
        return p.const_definition

    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement

    @_('break_statement')
    def statement(self, p):
        return p.break_statement

    @_('continue_statement')
    def statement(self, p):
        return p.continue_statement

    @_('expr SEMI')
    def statement(self, p):
        return p.expr
    
    @_('WHILE expr LBRACE statements RBRACE')
    def while_statement(self, p):
        return WhileStmt(p.expr, p.statements)

    @_('CONTINUE SEMI')
    def continue_statement(self, p):
        return ContinueStmt()

    @_('BREAK SEMI')
    def break_statement(self, p):
        return BreakStmt()

    @_('PRINT expr SEMI')
    def print_statement(self, p):
        return PrintStmt(p.expr, p.lineno)

    @_('location ASSIGN expr SEMI')
    def assignment_statement(self, p):
        return Assignment(p.location, p.expr, p.lineno)

    @_('VAR NAME [ type ] ASSIGN expr SEMI')
    def variable_definition(self, p):
        type_val = p.type
        expr_val = p.expr
        return VarDef(Name(p.NAME, p.lineno), type_val, expr_val, p.lineno)

    @_('VAR NAME type [ ASSIGN expr ] SEMI')
    def variable_definition(self, p):
        type_val = p.type
        expr_val = p.expr
        return VarDef(Name(p.NAME, p.lineno), type_val, expr_val, p.lineno)
    

    @_('CONST NAME [ type ] ASSIGN expr SEMI')
    def const_definition(self, p):
        if p.type:
            return ConstDef(Name(p.NAME, p.lineno), p.type, p.expr, p.lineno)
        else:
            return ConstDef(Name(p.NAME, p.lineno), None, p.expr, p.lineno)

    @_('IF expr LBRACE statements RBRACE [ ELSE LBRACE statements RBRACE ]')
    def if_statement(self, p):
        else_statements = None
        if p.ELSE:
            else_statements = ElseStmt(p.statements1, p.lineno) 

        return IfStmt(p.expr, p.statements0, else_statements, p.lineno)
            

    @_('expr PLUS expr')
    def expr(self, p):
        return BinOp(p.PLUS, p.expr0, p.expr1, p.lineno)

    @_('expr MINUS expr')
    def expr(self, p):
        return BinOp(p.MINUS, p.expr0, p.expr1, p.lineno)

    @_('expr TIMES expr')
    def expr(self, p):
        return BinOp(p.TIMES, p.expr0, p.expr1, p.lineno)
    
    @_('expr DIVIDE expr')
    def expr(self, p):
        return BinOp(p.DIVIDE, p.expr0, p.expr1, p.lineno)

    @_('expr LT expr')
    def expr(self, p):
        return BinOp(p.LT, p.expr0, p.expr1, p.lineno)

    @_('expr LE expr')
    def expr(self, p):
        return BinOp(p.LE, p.expr0, p.expr1, p.lineno)


    @_('expr GT expr')
    def expr(self, p):
        return BinOp(p.GT, p.expr0, p.expr1, p.lineno)

    @_('expr GE expr')
    def expr(self, p):
        return BinOp(p.GE, p.expr0, p.expr1, p.lineno)

    @_('expr EQ expr')
    def expr(self, p):
        return BinOp(p.EQ, p.expr0, p.expr1, p.lineno)

    @_('expr NE expr')
    def expr(self, p):
        return BinOp(p.NE, p.expr0, p.expr1, p.lineno)
    
    @_('expr LAND expr')
    def expr(self, p):
        return BinOp(p.LAND, p.expr0, p.expr1, p.lineno)

    @_('expr LOR expr')
    def expr(self, p):
        return BinOp(p.LOR, p.expr0, p.expr1, p.lineno)

    @_('PLUS expr %prec UPLUS')
    def expr(self, p):
        return UnaryOp(p.PLUS, p.expr, p.lineno)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return UnaryOp(p.MINUS, p.expr, p.lineno)

    @_('LNOT expr')
    def expr(self, p):
        return UnaryOp(p.LNOT, p.expr, p.lineno)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr


    @_('location')
    def expr(self, p):
        return p.location

    @_('literal')
    def expr(self, p):
        return p.literal

    @_('LBRACE statements RBRACE')
    def expr(self, p):
        return CompoundStmt(p.statements)

    @_('NAME')
    def location(self, p):
        return Name(p.NAME, p.lineno)

    @_('NAME')
    def type(self, p):
        return Type(p.NAME, p.lineno)

    @_('INTEGER')
    def literal(self, p):
        return Integer(p.INTEGER, p.lineno) 

    @_('FLOAT')
    def literal(self, p):
        return Float(p.FLOAT, p.lineno) 

    @_('CHAR')
    def literal(self, p):
        return Char(p.CHAR, p.lineno) 

    @_('LPAREN RPAREN')
    def literal(self, p):
        return Unit(p.lineno) 

    @_('TRUE')
    def literal(self, p):
        return Boolean(p.TRUE, p.lineno) 

    @_('FALSE')
    def literal(self, p):
        return Boolean(p.FALSE, p.lineno) 

def parse_tokens(tokens):
    
    parser = CalcParser()
    return parser.parse(tokens)



def parse_source(text):
    tokens = tokenize(text)
    model = parse_tokens(tokens)     # You need to implement this part
    return model
