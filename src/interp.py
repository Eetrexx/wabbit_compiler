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

def interpret_float(node, env):
    return node.value
    
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
        interpret(node.stmtlist, env)
    elif node.else_stmt:
        interpret(node.else_stmt, env)

def interpret_else_stmt(node, env):
    interpret(node.stmtlist, env)

def interpret_while_stmt(node, env):
    cond = interpret(node.cond, env)
    while cond:
        interpret(node.stmtlist, env)
        cond = interpret(node.cond, env)

# Internal function to interpret a node in the environment
def interpret(node, env):
    if isinstance(node, Integer):
        return interpret_integer(node, env)
    elif isinstance(node, Float):
        return interpret_float(node, env)
    elif isinstance(node, BinOp):
        return interpret_binop(node, env)
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
    # Expand to check for different node types
    # ...
    raise RuntimeError(f"Can't interpret {node}")
