import sys

from model import *
from interp import *
from tokenize import *
from parser import *
from typecheck import *

def main():
    op = sys.argv[1]
    file = sys.argv[2]

    if not op:
        raise RuntimeError(f'Missing operation to test')

    if not file:
        raise RuntimeError(f'Missing file to operate on')

    file = open(file)
    text = file.read()
#    model = parse_source(text)

    if op == "model":
        print(model)

    elif op == "interp":
        interpret_program(model)

    elif op == "tokenize":
        for tok in tokenize(text):
            print(tok)

    elif op == "typecheck":
        check_program(model)

    elif op == "codegen":
        pass

    else:
        raise RuntimeError(f'Unknown operation')


if __name__ == "__main__":
    main()
