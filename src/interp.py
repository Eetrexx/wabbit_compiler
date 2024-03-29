# Top level function that interprets an entire program. It creates the
# initial environment that's used for storing variables.
from model import *

def interpret_program(model):
    # Make the initial environment (a dict)
    env = { }
    env["const"] = { }
    env["var"] = { }
    interpret(model, env)

def interpret_integer(node, env):
    return node.value

def interpret_boolean(node, env):
    if node.value == "true":
        return True
    elif node.value == "false":
        return False

def interpret_float(node, env):
    return node.value

def interpret_unit(node, env):
    return None
    
def interpret_unaryop(node, env):
    value = interpret(node.expr, env)
    if node.op == '+':
        return 0 + value
    elif node.op == '-':
        return 0 - value
    elif node.op == '!':
        return not value
    else:
        raise RuntimeError(f'Error: unsupported unary operation')

def interpret_binop(node, env):
    leftval = interpret(node.left, env)
    rightval = interpret(node.right, env)
    assert type(leftval) == type(rightval)
    if node.op == '+':
        return leftval + rightval
    elif node.op == '-':
        return leftval - rightval
    elif node.op == '*':
        return leftval * rightval
    elif node.op == '/':
        return leftval / rightval
    elif node.op == '<':
        return leftval < rightval
    elif node.op == '>':
        return leftval > rightval
    elif node.op == '==':
        return leftval == rightval
    elif node.op == '!=':
        return leftval == rightval
    elif node.op == '>=':
        return leftval == rightval
    elif node.op == '<=':
        return leftval == rightval
    elif node.op == '&&':
        return leftval == rightval
    elif node.op == '||':
        return leftval == rightval
    # Expand to check for different operators
    # ...


def interpret_printstmt(node, env):
    print(f'{interpret(node.expr, env)}')


def interpret_name(node, env):
    if node.value in env["const"]:
        return env["const"][node.value]
    elif node.value in env["var"]:
        return env["var"][node.value]
    else:
        return None
    
def interpret_assignment(node, env):
    rightval = interpret(node.expr, env)
    leftval = interpret(node.location, env)

    if node.location.value in env["var"]:
        assert type(leftval) == type(rightval)
        env["var"][node.location.value] = rightval    
    elif node.location.value in env["const"]:
        raise RuntimeError(f"{node.location.value} is a constant")
    else:
        raise RuntimeError(f"{node.location.value} is not defined")
    

def interpret_statement(node, env):
    return interpret(node.expr, env)

def interpret_compound_stmt(node, env):
    for n in node.expr:
        ret_val = interpret(n, env)
        if ret_val in [ 'break', 'continue' ]:
            return ret_val
    return ret_val

def interpret_vardef(node, env):
    
    if node.expr:
        rightval = interpret(node.expr, env)
    else:
        if node.type.value == "float":
            rightval = 0.0
        else:
            rightval = 0
        
    env["var"][node.name.value] = rightval

def interpret_constdef(node, env):
    rightval = interpret(node.expr, env)
    env["const"][node.name.value] = rightval

def interpret_ifstmt(node, env):
    cond = interpret(node.cond, env)
    if cond:
        return interpret(node.stmtlist, env)
    elif node.else_stmt:
        return interpret(node.else_stmt, env)

def interpret_else_stmt(node, env):
    interpret(node.stmtlist, env)

def interpret_while_stmt(node, env):
    cond = interpret(node.cond, env)
    while cond:
        loop_exit = interpret(node.stmtlist, env)


        cond = interpret(node.cond, env)

        if loop_exit == "continue":
            continue
        elif loop_exit == "break":
            break
        else:
            pass


def interpret_continue_stmt(node, env):
    return "continue"

def interpret_break_stmt(node, env):
    return "break"

def interpret_char(node, env):
    return node.value

# Internal function to interpret a node in the environment
def interpret(node, env):
    if isinstance(node, Integer):
        return interpret_integer(node, env)
    elif isinstance(node, Float):
        return interpret_float(node, env)
    elif isinstance(node, Boolean):
        return interpret_boolean(node, env)
    elif isinstance(node, Unit):
        return interpret_unit(node, env)
    elif isinstance(node, BinOp):
        return interpret_binop(node, env)
    elif isinstance(node, UnaryOp):
        return interpret_unaryop(node, env)
    elif isinstance(node, Name):
        return interpret_name(node, env)
    elif isinstance(node, Statement):
        return interpret_statement(node, env)
    elif isinstance(node, CompoundStmt):
        return interpret_compound_stmt(node, env)
    elif isinstance(node, PrintStmt):
        return interpret_printstmt(node, env)
    elif isinstance(node, Assignment):
        return interpret_assignment(node, env)
    elif isinstance(node, VarDef):
        return interpret_vardef(node, env)
    elif isinstance(node, ConstDef):
        return interpret_constdef(node, env)
    elif isinstance(node, IfStmt):
        return interpret_ifstmt(node, env)
    elif isinstance(node, ElseStmt):
        return interpret_else_stmt(node, env)
    elif isinstance(node, WhileStmt):
        return interpret_while_stmt(node, env)
    elif isinstance(node, ContinueStmt):
        return interpret_continue_stmt(node, env)
    elif isinstance(node, BreakStmt):
        return interpret_break_stmt(node, env)
    elif isinstance(node, Char):
        return interpret_char(node, env)
    # Expand to check for different node types
    # ...
    raise RuntimeError(f"Can't interpret {node}")
