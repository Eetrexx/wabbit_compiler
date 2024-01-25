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

def to_source_list(node_list):
    ret_str = ""
    for node in node_list:
        ret_str += f'''{to_source(node)}\n''' 

    return ret_str

def to_source_neo(node_list):
    ret_str = ""
    for node in node_list:
        ret_str += f'''    {to_source(node)}\n'''

    return ret_str
def to_source_singleline(node_list):
    ret_str = ""
    for node in node_list:
        ret_str += f' {to_source(node)} ' 

    return ret_str

def to_source(node):

    if isinstance(node, Integer):
        return str(node.value)
    elif isinstance(node, Float):
        return repr(node.value)
    elif isinstance(node, Unit):
        return f'()'
    elif isinstance(node, Boolean):
        return repr(node.value)
    elif isinstance(node, Name):
        return str(node.value)
    elif isinstance(node, Statement):
        return f'{to_source(node.expr)};'
    elif isinstance(node, CompoundStmt):
        return f'{to_source_list(node.expr)}' 
    elif isinstance(node, Type):
        return str(node.value)
    elif isinstance(node, UnaryOp):
        return "" + node.op + to_source(node.expr)
    elif isinstance(node, BinOp):
        return f'{to_source(node.left)} {node.op} {to_source(node.right)}'
    elif isinstance(node, PrintStmt):
        return f'print {to_source(node.expr)};'
    elif isinstance(node, ConstDef):
        return f'const {to_source(node.name)} = {to_source(node.expr)};'
    elif isinstance(node, VarDef):
        if node.expr is None:
            return f'var {to_source(node.name)} {to_source(node.type)};'
        elif node.type is None:
            return f'var {to_source(node.name)} = {to_source(node.expr)};'
        else:
            return f'var {to_source(node.name)} {to_source(node.type)} = {to_source(node.expr)};'
    elif isinstance(node, Assignment):
        return f'{to_source(node.location)} = {to_source(node.expr)};'
    elif isinstance(node, IfStmt):
        if node.else_stmt is None:
            return f'''if {to_source(node.cond)} {{\n{to_source_list(node.stmtlist)}}}'''
        else:
            return f'if {to_source(node.cond)} {{\n{to_source_list(node.stmtlist)}}} {to_source(node.else_stmt)}'

    elif isinstance(node, ElseStmt):
        return f'else {{\n{to_source_list(node.stmtlist)}}}'
    elif isinstance(node, WhileStmt):
        
        return f'''while {to_source(node.cond)} {{\n{to_source_neo(node.stmtlist.expr)}}}'''
    elif isinstance(node, ContinueStmt):
        return f'continue;'
    elif isinstance(node, BreakStmt):
        return f'break;'
    else:
        raise RuntimeError(f"Can't convert {node} to source")
