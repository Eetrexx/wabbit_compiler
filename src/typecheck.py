from model import *
# Top-level function used to check programs


has_errors = False

def error_msg(lineno, text):

    print(f'{lineno}: {text}')
    has_errors = True

def check_program(model):
    env = { }
    env["const"] = { }
    env["var"] = { }

    check(model, env, 0)
    # Maybe return True/False if there are errors

    return not has_errors

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
   # ('unit', '!=', 'char') : 'bool',
   # ('unit', '==', 'char') : 'bool',
   # ('char', '==', 'unit') : 'bool',
   # ('char', '!=', 'unit') : 'bool',
   # ('unit', '!=', 'int') : 'bool',
   # ('unit', '==', 'int') : 'bool',
   # ('int', '==', 'unit') : 'bool',
   # ('int', '!=', 'unit') : 'bool',
   # ('unit', '!=', 'float') : 'bool',
   # ('unit', '==', 'float') : 'bool',
   # ('float', '==', 'unit') : 'bool',
   # ('float', '!=', 'unit') : 'bool',
   # ('unit', '!=', 'bool') : 'bool',
   # ('unit', '==', 'bool') : 'bool',
   # ('bool', '==', 'unit') : 'bool',
   # ('bool', '!=', 'unit') : 'bool',
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

def check_unaryop(node, env, in_while):
    expr = check(node.expr, env, in_while)
    result_type = _unaryops.get((node.op, expr))

    if result_type is None:
        text = f"Unsupported operation: {node.op}{expr}"
        error_msg(node.expr.lineno, text)

    return result_type

def check_binop(node, env, in_while):
    left_type = check(node.left, env, in_while)
    right_type = check(node.right, env, in_while)

    result_type = _binops.get((left_type, node.op, right_type))
    if result_type is None:
        text = f"Unsupported operation: {left_type} {node.op} {right_type}"
        error_msg(node.left.lineno, text)

    return result_type


def check_declaration(node, env, in_while):
    if node.expr:
        right_type = check(node.expr, env, in_while)

        if node.type:
            if node.type.value != right_type:
                text = f"Type error in initialization. {node.type.value} != {right_type}"
                error_msg(node.lineno, text)
                return None 
            

        if isinstance(node, VarDef):
            if node.name.value in env["var"]:
                text = f"{node.name.value} already defined!"
                error_msg(node.lineno, text)
                return None
            env["var"][node.name.value] = right_type
        elif isinstance(node, ConstDef):
            env["const"][node.name.value] = right_type
    elif node.type:
        if isinstance(node, VarDef):
            if node.name.value in env["var"]:
                text = f"{node.name.value} already defined!"
                error_msg(node.lineno, text)
                return None
            env["var"][node.name.value] = node.type.value 
        elif isinstance(node, ConstDef):
            error_msg(node.lineno, "Error: const declaration expects a value")
            return None 
    else:
        error_msg(node.lineno, "Error: variable declaration without any type or value")
        return None 

def check_assignment(node, env, in_while):
    left_type = check(node.location, env, in_while)
    right_type = check(node.expr, env, in_while)
    
    if left_type:
        if node.location.value in env["const"]:
            text = f"Can't assign to const"
            error_msg(node.lineno, text)
            return None

        elif left_type != right_type:
            text = f"Type error in assignment. {left_type} != {right_type}"
            error_msg(node.lineno, text)
            return None

        else:
            env["var"][node.location.value] = right_type


def check_name(node, env, in_while):
    ret_val = None
    if node.value in env["const"]:
        ret_val = env["const"][node.value]
    elif node.value in env["var"]:
        ret_val = env["var"][node.value]
    else:
        text = f"{node.value} not defined!"
        error_msg(node.lineno, text)

    return ret_val

def check_if_stmt(node, env, in_while):
    test = check(node.cond, env, in_while)

    if test != "bool":
        text = f"if test must be bool. Got {test}"
        error_msg(node.lineno, text)
    
    check(node.stmtlist, env, in_while)
    check(node.else_stmt, env, in_while)
    
def check_else_stmt(node, env, in_while):
    check(node.stmtlist, env, in_while)

def check_stmt(node, env, in_while):
    return check(node, env, in_while)

def check_compound_stmt(node, env, in_while):
    for n in node.expr:
        ret_val = check(n, env, in_while)
    return ret_val

def check_while_stmt(node, env, in_while):
    
    test = check(node.cond, env, in_while)

    if test != "bool":
        text = f"while test must be bool. Got {test}"
        error_msg(node.lineno, text)

    in_while += 1
    check(node.stmtlist, env, in_while)
    in_while -= 1

def check_print_stmt(node, env, in_while):
    check(node.expr, env, in_while)

def check_continue_stmt(node, env, in_while):
    if in_while == 0:
        text = f"continue used outside of while loop"
        error_msg(node.lineno, text)

def check_break_stmt(node, env, in_while):
    if in_while == 0:
        text = f"break used outside of while loop"
        error_msg(node.lineno, text)

def check_integer(node, env, in_while):
    return "int"

def check_float(node, env, in_while):
    return "float"

def check_boolean(node, env, in_while):
    return "bool"

def check_char(node, env, in_while):
    return "char"

def check_unit(node, env, in_while):
    return "unit"

# Internal function used to check nodes with an environment
def check(node, env, in_while):
    if isinstance(node, list):
        for i in node:
            check(i, env, in_while)
    elif isinstance(node, Integer):
        return check_integer(node, env, in_while)
    elif isinstance(node, Float):
        return check_float(node, env, in_while)
    elif isinstance(node, Boolean):
        return check_boolean(node, env, in_while)
    elif isinstance(node, Unit):
        return check_unit(node, env, in_while)
    elif isinstance(node, BinOp):
        return check_binop(node, env, in_while)
    elif isinstance(node, UnaryOp):
        return check_unaryop(node, env, in_while)
    elif isinstance(node, Name):
        return check_name(node, env, in_while)
    elif isinstance(node, Statement):
        return check_stmt(node, env, in_while)
    elif isinstance(node, CompoundStmt):
        return check_compound_stmt(node, env, in_while)
    elif isinstance(node, PrintStmt):
        return check_print_stmt(node, env, in_while)
    elif isinstance(node, Assignment):
        return check_assignment(node, env, in_while)
    elif isinstance(node, VarDef):
        return check_declaration(node, env, in_while)
    elif isinstance(node, ConstDef):
        return check_declaration(node, env, in_while)
    elif isinstance(node, IfStmt):
        return check_if_stmt(node, env, in_while)
    elif isinstance(node, ElseStmt):
        return check_else_stmt(node, env, in_while)
    elif isinstance(node, WhileStmt):
        return check_while_stmt(node, env, in_while)
    elif isinstance(node, ContinueStmt):
        return check_continue_stmt(node, env, in_while)
    elif isinstance(node, BreakStmt):
        return check_break_stmt(node, env, in_while)
    elif isinstance(node, Char):
        return check_char(node, env, in_while)
    else:
        pass
