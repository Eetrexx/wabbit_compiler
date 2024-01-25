# A Compiler for Wabbit

This is a compiler for the Wabbit language. It is written in python and will compile to LLVM instructions. 
The code for each part of the compiler is in the python modules located at the `src` folder.

Currently, the compiler itself is incomplete. You can run each module separately with the test modules. In the future, you will be able to use the complete compiler module to create executable code.

In order to test each working module, you must run the `test` module in the `tests` folder inside the `src` folder as the following:

`python -m tests.test <compiler_step> <file>`

Where `<compiler_step>` is the part of the compiler you want to test, and `<file>` is the wabbit source code to test.

Currently implemented compiler steps are `model`, `interp`, `typecheck` and `tokenize`. The compiler uses the `parser` step internally.
