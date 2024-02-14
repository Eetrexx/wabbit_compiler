
class Node:
    def __init__(self, lineno):
        self.lineno = lineno



class Char(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Char({self.value})'

    def __str__(self):
        return self.value

class Unit(Node):
    def __init__(self, lineno):
        self.value = "()"
        super().__init__(lineno)

    def __repr__(self):
        return f'Unit()'

class Boolean(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Boolean({self.value})'

    def __str__(self):
        return self.value
    
class Type(Node):

    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Type({self.value})'

    def __str__(self):
        return self.value
    
    
class Name(Node):

    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Name({self.value})'
        
    def __str__(self):
        return self.value
        
class Integer(Node):
    '''
    Example: 42
    '''
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Integer({self.value})'

    def __str__(self):
        return str(self.value)

class Float(Node):
    '''
    Example: 42
    '''
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)

    def __repr__(self):
        return f'Float({self.value})'

class UnaryOp(Node):

    def __init__(self, op, expr, lineno):
        self.op = op
        self.expr = expr
        super().__init__(lineno)

    def __repr__(self):
        return f'UnaryOp({self.op}, {self.expr})'

class BinOp(Node):
    '''
    Example: left + right
    '''
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        super().__init__(lineno)

    def __repr__(self):
        return f'BinOp({self.op}, {self.left}, {self.right})'

class PrintStmt(Node):

    def __init__(self, expr, lineno):
        self.expr = expr
        super().__init__(lineno)

    def __repr__(self):
        return f'PrintStmt({self.expr})'


class Const(Node):
    def __init__(self, name, lineno):
        self.name = name
        super().__init__(lineno)

    def __repr__(self):
        return f'Const({self.name})'

class Variable(Node):
    def __init__(self, name, lineno):
        self.name = name
        super().__init__(lineno)

    def __repr__(self):
        return f'Variable({self.name})'
    
class CompoundStmt:
    
    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f'CompoundStmt({self.expr})'

class Statement(Node):

    def __init__(self, expr, lineno):
        self.expr = expr
        super().__init__(lineno)
        
    def __repr__(self):
        return f'Statement({self.expr})'

class ConstDef(Node):

    def __init__(self, name, type=None, expr=None, lineno=None):
        self.name = name
        self.type = type
        self.expr = expr
        super().__init__(lineno)

    def __repr__(self):
        return f'ConstDef({self.name}, {self.type}, {self.expr})'

class VarDef(Node):
    
    def __init__(self, name, type=None, expr=None, lineno=None):
        self.name = name
        self.type = type
        self.expr = expr
        super().__init__(lineno)

    def __repr__(self):
        return f'VarDef({self.name}, {self.type}, {self.expr})'

class Assignment(Node):

    def __init__(self, location, expr, lineno):
        self.location = location
        self.expr = expr
        super().__init__(lineno)

    def __repr__(self):
        return f'Assignment({self.location}, {self.expr})'

class ContinueStmt:
    def __repr__(self):
        return f'ContinueStmt()'

class BreakStmt:
    def __repr__(self):
        return f'BreakStmt()'

class IfStmt(Node):

    def __init__(self, cond, stmtlist, else_stmt=None, lineno=None):
        self.cond = cond
        self.stmtlist = stmtlist
        self.else_stmt = else_stmt
        super().__init__(lineno)

    def __repr__(self):
        return f'IfStmt({self.cond}, {self.stmtlist}, {self.else_stmt})'

class ElseStmt(Node):
    
    def __init__(self, stmtlist, lineno):
        
        self.stmtlist = stmtlist
        super().__init__(lineno)
        

    def __repr__(self):
        return f'ElseStmt({self.stmtlist})'
    

class WhileStmt:

    def __init__(self, cond, stmtlist):
        self.cond = cond
        self.stmtlist = stmtlist
        

    def __repr__(self):
        return f'WhileStmt({self.cond}, {self.stmtlist})'
    
# ------ Debugging function to convert a model into source code (for easier viewing)


def to_source_list(node_list, rec_level):
    ret_str = ""
    ident_spaces = "    "
    for node in node_list:
        n = 0
        while n < rec_level:
            ret_str += ident_spaces
            n+=1
        ret_str += f'''{to_source_internal(node, rec_level)}\n''' 

    return ret_str

def to_source_singleline(node_list, rec_level):
    ret_str = ""
    for node in node_list:
        ret_str += f' {to_source_internal(node, rec_level)}' 
        #print(type(node)) 
        if isinstance(node, Integer) or isinstance(node, Float) or isinstance(node, Char) or isinstance(node, Boolean) or isinstance(node, Unit) or isinstance(node, BinOp) or isinstance(node, Name):
            ret_str += ";"

    ret_str += f' '

    return ret_str

def to_source(node):
    return to_source_internal(node, 0)

def to_source_internal(node, rec_level):

    if isinstance(node, list):
        return f'{to_source_list(node, rec_level)}'
    elif isinstance(node, Integer):
        return str(node.value)
    elif isinstance(node, Char):
        return node.value
    elif isinstance(node, Float):
        return str(node.value)
    elif isinstance(node, Unit):
        return f'()'
    elif isinstance(node, Boolean):
        return str(node.value)
    elif isinstance(node, Name):
        return str(node.value)
    elif isinstance(node, Statement):
        return f'{to_source_internal(node.expr, rec_level)};'
    elif isinstance(node, CompoundStmt):
        return f'{{{to_source_singleline(node.expr, rec_level)}}}' 
    elif isinstance(node, Type):
        return str(node.value)
    elif isinstance(node, UnaryOp):
        return "" + node.op + to_source_internal(node.expr, rec_level)
    elif isinstance(node, BinOp):
        return f'{to_source_internal(node.left, rec_level)} {node.op} {to_source_internal(node.right, rec_level)}'
    elif isinstance(node, PrintStmt):
        return f'print {to_source_internal(node.expr, rec_level)};'
    elif isinstance(node, ConstDef):
        return f'const {to_source_internal(node.name, rec_level)} = {to_source_internal(node.expr, rec_level)};'
    elif isinstance(node, VarDef):
        if node.expr is None:
            return f'var {to_source_internal(node.name, rec_level)} {to_source_internal(node.type, rec_level)};'
        elif node.type is None:
            return f'var {to_source_internal(node.name, rec_level)} = {to_source_internal(node.expr, rec_level)};'
        else:
            return f'var {to_source_internal(node.name, rec_level)} {to_source_internal(node.type, rec_level)} = {to_source_internal(node.expr, rec_level)};'
    elif isinstance(node, Assignment):
        return f'{to_source_internal(node.location, rec_level)} = {to_source_internal(node.expr, rec_level)};'
    elif isinstance(node, IfStmt):
        ret_str = f'if {to_source_internal(node.cond, rec_level)} {{\n'
        rec_level += 1
        ret_str += f'{to_source_list(node.stmtlist, rec_level)}'
        rec_level -= 1
        n = 0
        while n < rec_level:
            ret_str += "    "
            n += 1
        ret_str += "}"

        if node.else_stmt:
            ret_str += f' {to_source_internal(node.else_stmt, rec_level)}'

        return ret_str

    elif isinstance(node, ElseStmt):
        ret_str = f'else {{\n'
        rec_level += 1
        ret_str += f'{to_source_list(node.stmtlist, rec_level)}'
        rec_level -= 1
        n = 0
        while n < rec_level:
            ret_str += "    "
            n += 1
        ret_str += "}"
        return ret_str 
    elif isinstance(node, WhileStmt):
       
        ret_str = f'while {to_source_internal(node.cond, rec_level)} {{\n'
        rec_level += 1
        ret_str += f'{to_source_list(node.stmtlist, rec_level)}'
        rec_level -= 1
        n = 0
        while n < rec_level:
            ret_str += "    "
            n += 1
        ret_str += "}"
        return ret_str

    elif isinstance(node, ContinueStmt):
        return f'continue;'
    elif isinstance(node, BreakStmt):
        return f'break;'
    else:
        raise RuntimeError(f"Can't convert {node} to source")
