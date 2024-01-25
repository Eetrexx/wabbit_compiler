# Top-level function that runs everything
from model import *
from tokenize import *
class TokenList:
    def __init__(self):
        self.index = 0
        self.items = []
        self.max_tokens = 0


def parse_factor(tokens):
    if tokens.items[tokens.index].type == 'INTEGER':
        ret = Integer(int(tokens.items[tokens.index].value))
    elif tokens.items[tokens.index].type == 'FLOAT':
        ret = Float(float(tokens.items[tokens.index].value))
    elif tokens.items[tokens.index].type in ['TRUE', 'FALSE']:
        ret = Boolean(tokens.items[tokens.index].value)
    elif tokens.items[tokens.index].type == 'NAME':
        ret = Name(f'{tokens.items[tokens.index].value}')
    elif tokens.items[tokens.index].type == 'CHAR':
        ret = Char(f'{tokens.items[tokens.index].value}')
    elif tokens.items[tokens.index].type == 'LPAREN':
        if tokens.items[tokens.index+1].type == 'RPAREN':
            ret = Unit()
            tokens.index += 1
        else:
            tokens.index += 1
            ret = parse_cond(tokens)
            if tokens.items[tokens.index].type != 'RPAREN':
                raise RuntimeError(f'Error at line {tokens.items[tokens.index].lineno} - Missing ")"')
        
    else:
        raise RuntimeError(f'Error parsing token (at line {tokens.items[tokens.index].lineno} - {tokens.items[tokens.index]})- invalid literal {tokens.items[tokens.index].value}')

    tokens.index += 1
    return ret

def parse_unary(tokens):
    op = tokens.items[tokens.index].type in ['LNOT', 'PLUS', 'MINUS']

    if not op:
        return parse_factor(tokens)
    else:
        op = tokens.items[tokens.index].value
        tokens.index += 1
        return UnaryOp(op, parse_factor(tokens))
        

def parse_term(tokens):
    unary = parse_unary(tokens)
    while True:
        op = tokens.items[tokens.index].type in ['TIMES', 'DIVIDE']
        if not op:
            return unary 
        else:
            op = tokens.items[tokens.index].value
            tokens.index += 1
        unary = BinOp(op, unary, parse_unary(tokens))

def parse_expression(tokens):
    term = parse_term(tokens)
    while True:
        op = tokens.items[tokens.index].type in ['PLUS', 'MINUS']
        if not op:
            return term
        else:
            op = tokens.items[tokens.index].value
            tokens.index += 1

        term = BinOp(op, term, parse_term(tokens))

def parse_cond(tokens):
    expr = parse_expression(tokens)
    while True:
        op = tokens.items[tokens.index].type in ['LE', 'GE', 'LT', 'GT', 'EQ', 'LOR', 'LAND', 'NE']
        if not op:
            return expr
        else:
            op = tokens.items[tokens.index].value
            tokens.index += 1

        expr = BinOp(op, expr, parse_expression(tokens))

def parse_print_statement(tokens):
    tokens.index += 1
    expr = parse_cond(tokens)
    
    if tokens.items[tokens.index].type != 'SEMI':
        raise RuntimeError(f'Error at line number {tokens.items[tokens.index].lineno}: expected ; at the end')
    tokens.index += 1
    return PrintStmt(expr)

def parse_var_def(tokens):
    tokens.index += 1
    if tokens.items[tokens.index].type == 'NAME':
        if tokens.items[tokens.index+1].value in ['int', 'float', 'char', 'bool']:
            if tokens.items[tokens.index+2].type == 'SEMI':
                
                name = Name(f'{tokens.items[tokens.index].value}')
                type = Type(f'{tokens.items[tokens.index+1].value}')
                vardef = VarDef(name, type, None)
                tokens.index += 3
            elif tokens.items[tokens.index+2].type == 'ASSIGN':
                name = Name(f'{tokens.items[tokens.index].value}')
                type = Type(f'{tokens.items[tokens.index+1].value}')
                tokens.index += 3
                vardef = VarDef(name, type, parse_cond(tokens))

            else:
                raise RuntimeError(f'Error on lineno {tokens.items[tokens.index].lineno} - invalid variable declaration')
        elif tokens.items[tokens.index+1].type == 'ASSIGN':
            name = Name(f'{tokens.items[token.index].value}')
            tokens += 2
            vardef = VarDef(name, None, parse_cond(tokens))
        else:
            raise RuntimeError(f'Error on lineno {tokens.items[tokens.index].lineno} - invalid variable type')
    else:
        raise RuntimeError(f'Error on lineno {tokens.items[tokens.index].lineno} - invalid variable name')
    return vardef

def parse_const_def(tokens):
    
    tokens.index += 1
    constdef = None
    if tokens.items[tokens.index].type == 'NAME':
        if tokens.items[tokens.index+1].value in ['int', 'float','char','bool']:
            if tokens.items[tokens.index+2].type == 'ASSIGN':
                name = Name(f'{tokens.items[tokens.index].value}')
                type = Type(f'{tokens.items[tokens.index+1].value}')
                tokens.index += 3
                constdef = ConstDef(name, type, parse_cond(tokens))
                
        elif tokens.items[tokens.index+1].type == 'ASSIGN':
            name = tokens.items[tokens.index].value
            tokens.index += 2
            constdef = ConstDef(name, None, parse_cond(tokens))
        else:
            raise RuntimeError(f'Error on lineno {tokens[0].lineno} - invalid constant definition')
    else:
        raise RuntimeError(f'Error on lineno {tokens[0].lineno} - invalid constant name')
    return constdef

def parse_if_statement(tokens):
    else_statement = None
    tokens.index += 1
    cond = parse_cond(tokens)
    if tokens.items[tokens.index].type == 'LBRACE':
        statements = parse_compound_statement(tokens)

    if tokens.items[tokens.index].type == 'ELSE':
        else_statement = parse_else_statement(tokens)
    
    return IfStmt(cond, statements, else_statement)

def parse_else_statement(tokens):
    tokens.index += 1
    
    if tokens.items[tokens.index].type == 'LBRACE':
        statements = parse_compound_statement(tokens)
    elif tokens.items[tokens.index].type == 'IF':
        statements = parse_if_statement(tokens)

    return ElseStmt(statements)

def parse_while_statement(tokens):

    tokens.index += 1
    cond = parse_cond(tokens)
    
    if tokens.items[tokens.index].type == 'LBRACE':
        statements = parse_compound_statement(tokens)

    return WhileStmt(cond, statements)


def parse_assignment(tokens):
    name = Name(f'{tokens.items[tokens.index].value}')

    tokens.index += 2
    ret_val = Assignment(name, parse_cond(tokens))

    return ret_val

def parse_continue_statement(tokens):
    ret_val = ContinueStmt()
    tokens.index += 2
    return ret_val

def parse_break_statement(tokens):
    ret_val = BreakStmt()
    tokens.index += 2
    return ret_val

def parse_statement(tokens):
    ret_val = None
    
    if tokens.index < tokens.max_tokens:
        if tokens.items[tokens.index].type == 'PRINT':
            ret_val = parse_print_statement(tokens)
        elif tokens.items[tokens.index].type == 'VAR':
            ret_val = parse_var_def(tokens)
        elif tokens.items[tokens.index].type == 'CONST':
            ret_val = parse_const_def(tokens)
        elif tokens.items[tokens.index].type == 'NAME':
            if tokens.items[tokens.index+1].type == 'ASSIGN':
                ret_val = parse_assignment(tokens)
        elif tokens.items[tokens.index].type == 'IF':
            ret_val = parse_if_statement(tokens)
        elif tokens.items[tokens.index].type == 'WHILE':
            ret_val = parse_while_statement(tokens)
        elif tokens.items[tokens.index].type == 'BREAK':
            ret_val = parse_break_statement(tokens)
        elif tokens.items[tokens.index].type == 'CONTINUE':
            ret_val = parse_continue_statement(tokens)
        elif tokens.items[tokens.index].type == 'ELSE':
            ret_val = parse_else_statement(tokens)
        else:
            tokens.index += 1
        
    return ret_val

def parse_compound_statement(tokens):
    ret_val = []
    
    if tokens.items[tokens.index].type == 'LBRACE':
        tokens.index += 1
        i_count = tokens.index
        range_count = 0
        while tokens.items[i_count].type != 'RBRACE':
            range_count += 1
            i_count += 1
        while range_count > 0:
            add_item = parse_statement(tokens)
            if add_item:
                ret_val.append(add_item)
            range_count -= 1

    else:
         while tokens.index < tokens.max_tokens:
            add_item = parse_statement(tokens)
            if add_item:
                ret_val.append(add_item)

    return CompoundStmt(ret_val)


def parse_tokens(tokens):
    
    return parse_compound_statement(tokens)

    

def parse_source(text):
    tokens = TokenList()
    
    for tok in tokenize(text):
        tokens.items.append(tok)
        tokens.max_tokens += 1

    model = parse_tokens(tokens)     # You need to implement this part
    return model
