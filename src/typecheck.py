from model import *
# Top-level function used to check programs
def check_program(model):
    env = { }
    env["const"] = { }
    env["var"] = { }

    check(model, env)
    # Maybe return True/False if there are errors

_binops = {
    # ('lefttype', 'op', 'righttype') : 'resulttype'
    ('int', '+', 'int') : 'int',
    ('int', '-', 'int') : 'int',
    ('int', '*', 'int') : 'int',
    ('int', '/', 'int') : 'int',
    ('int', '>', 'int') : 'bool',
    ('int', '<', 'int') : 'bool',
    ('int', '<=', 'int') : 'bool',
    ('int', '>=', 'int') : 'bool',
    ('int', '==', 'int') : 'bool',
    ('int', '!=', 'int') : 'bool',
    ('float', '+', 'float') : 'float',
    ('float', '-', 'float') : 'float',
    ('float', '*', 'float') : 'float',
    ('float', '/', 'float') : 'float',
    ('float', '>', 'float') : 'bool',
    ('float', '>=', 'float') : 'bool',
    ('float', '<', 'float') : 'bool',
    ('float', '<=', 'float') : 'bool',
    ('float', '==', 'float') : 'bool',
    ('float', '!=', 'float') : 'bool',
    ('bool', '==', 'bool') : 'bool',
    ('bool', '&&', 'bool') : 'bool',
    ('bool', '||', 'bool') : 'bool',
    ('char', '>', 'char') : 'bool',
    ('char', '<', 'char') : 'bool',
    ('char', '==', 'char') : 'bool',
    ('char', '!=', 'char') : 'bool',
    ('unit', '!=', 'char') : 'bool',
    ('unit', '==', 'char') : 'bool',
    ('char', '==', 'unit') : 'bool',
    ('char', '!=', 'unit') : 'bool',
    ('unit', '!=', 'int') : 'bool',
    ('unit', '==', 'int') : 'bool',
    ('int', '==', 'unit') : 'bool',
    ('int', '!=', 'unit') : 'bool',
    ('unit', '!=', 'float') : 'bool',
    ('unit', '==', 'float') : 'bool',
    ('float', '==', 'unit') : 'bool',
    ('float', '!=', 'unit') : 'bool',
    ('unit', '!=', 'bool') : 'bool',
    ('unit', '==', 'bool') : 'bool',
    ('bool', '==', 'unit') : 'bool',
    ('bool', '!=', 'unit') : 'bool',
    ('unit', '!=', 'unit') : 'bool',
    ('unit', '==', 'unit') : 'bool'
}

_unaryops = {
        ('!', 'bool') : 'bool', 
        ('+', 'int') : 'int', 
        ('-', 'int') : 'int', 
        ('+', 'float') : 'float', 
        ('-', 'float') : 'float' 
}

def check_unaryop(node, env):
    expr = check(node.expr, env)
    result_type = _unaryops.get((node.op, expr))

    if result_type is None:
        raise RuntimeError(f'Error: unsupported unary operation')

    return result_type

def check_binop(node, env):
    left_type = check(node.left, env)
    right_type = check(node.right, env)

    result_type = _binops.get((left_type, node.op, right_type))
    if result_type is None:
        raise RuntimeError(f"Type mismatch! {left_type} {node.op} {right_type}")

    return result_type


def check_declaration(node, env):
    if node.expr:
        right_type = check(node.expr, env)

        if node.type:
            if node.type.value != right_type:
                raise RuntimeError(f'Error: expected {node.type} on variable declaration - got {right_type}' )
        if isinstance(node, VarDef):
            env["var"][node.name.value] = right_type
        elif isinstance(node, ConstDef):
            env["const"][node.name.value] = right_type
    elif node.type:
        if isinstance(node, VarDef):
            env["var"][node.name.value] = node.type.value 
        elif isinstance(node, ConstDef):
            raise RuntimeError(f'Error: const declaration expects a value')
    else:
        raise RuntimeError(f'Error: variable declaration without any type or value')

def check_assignment(node, env):
    left_type = check(node.location, env)
    right_type = check(node.expr, env)

    if left_type != right_type:
        raise RuntimeError(f"Error: incompatible types in assignment ({left_type} and {right_type})")

def check_name(node, env):
    ret_val = None
    if node.value in env["const"]:
        ret_val = env["const"][node.value]
    elif node.value in env["var"]:
        ret_val = env["var"][node.value]
    else:
        raise RuntimeError(f"Error: {node.value} is not defined")
    return ret_val

def check_if_stmt(node, env):
    check(node.cond, env)
    check(node.stmtlist, env)
    check(node.else_stmt, env)
    
def check_else_stmt(node, env):
    check(node.stmtlist, env)

def check_stmt(node, env):
    return check(node, env)

def check_compound_stmt(node, env):
    for n in node.expr:
        ret_val = check(n, env)
    return ret_val

def check_while_stmt(node, env):
    check(node.cond, env)
    check(node.stmtlist, env)

def check_print_stmt(node, env):
    check(node.expr, env)

def check_continue_stmt(node, env):
    pass

def check_break_stmt(node, env):
    pass

def check_integer(node, env):
    return "int"

def check_float(node, env):
    return "float"

def check_boolean(node, env):
    return "bool"

def check_char(node, env):
    return "char"

def check_unit(node, env):
    return "unit"

# Internal function used to check nodes with an environment
def check(node, env):
    if isinstance(node, Integer):
        return check_integer(node, env)
    elif isinstance(node, Float):
        return check_float(node, env)
    elif isinstance(node, Boolean):
        return check_boolean(node, env)
    elif isinstance(node, Unit):
        return check_unit(node, env)
    elif isinstance(node, BinOp):
        return check_binop(node, env)
    elif isinstance(node, UnaryOp):
        return check_unaryop(node, env)
    elif isinstance(node, Name):
        return check_name(node, env)
    elif isinstance(node, Statement):
        return check_stmt(node, env)
    elif isinstance(node, CompoundStmt):
        return check_compound_stmt(node, env)
    elif isinstance(node, PrintStmt):
        return check_print_stmt(node, env)
    elif isinstance(node, Assignment):
        return check_assignment(node, env)
    elif isinstance(node, VarDef):
        return check_declaration(node, env)
    elif isinstance(node, ConstDef):
        return check_declaration(node, env)
    elif isinstance(node, IfStmt):
        return check_if_stmt(node, env)
    elif isinstance(node, ElseStmt):
        return check_else_stmt(node, env)
    elif isinstance(node, WhileStmt):
        return check_while_stmt(node, env)
    elif isinstance(node, ContinueStmt):
        return check_continue_stmt(node, env)
    elif isinstance(node, BreakStmt):
        return check_break_stmt(node, env)
    elif isinstance(node, Char):
        return check_char(node, env)
    else:
        pass
