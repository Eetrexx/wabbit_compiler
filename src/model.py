class Char:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Char({self.value})'

class Type:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Type({self.value})'

    def __str__(self):
        return self.value
    
    
class Name:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Name({self.value})'
        
    def __str__(self):
        return self.value
        
class Integer:
    '''
    Example: 42
    '''
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Integer({self.value})'

    def __str__(self):
        return str(self.value)

class Float:
    '''
    Example: 42
    '''
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Float({self.value})'

class BinOp:
    '''
    Example: left + right
    '''
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinOp({self.op}, {self.left}, {self.right})'

class PrintStmt:

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f'PrintStmt({self.expr})'


class Const:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Const({self.name})'

class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Variable({self.name})'
    
class CompoundStmt:
    
    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f'CompoundStmt({self.expr})'
class Statement:

    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f'Statement({self.expr})'

class ConstDef:

    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f'ConstDef({self.name}, {self.expr})'

class VarDef:
    
    def __init__(self, name, type=None, expr=None):
        self.name = name
        self.type = type
        self.expr = expr

    def __repr__(self):
        return f'VarDef({self.name}, {self.type}, {self.expr})'

class Assignment:

    def __init__(self, location, expr):
        self.location = location
        self.expr = expr

    def __repr__(self):
        return f'Assignment({self.location}, {self.expr})'

class IfStmt:

    def __init__(self, cond, stmtlist, else_stmt=None):
        self.cond = cond
        self.stmtlist = stmtlist
        self.else_stmt = else_stmt

    def __repr__(self):
        return f'IfStmt({self.cond}, {self.stmtlist}, {self.else_stmt})'

class ElseStmt:
    
    def __init__(self, stmtlist):
        
        self.stmtlist = stmtlist
        

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
    elif isinstance(node, Name):
        return str(node.value)
    elif isinstance(node, Statement):
        return f'{to_source(node.expr)};'
    elif isinstance(node, CompoundStmt):
        return f'{to_source_list(node.expr)}' 
    elif isinstance(node, Type):
        return str(node.value)
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
    else:
        raise RuntimeError(f"Can't convert {node} to source")
