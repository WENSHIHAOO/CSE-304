Run: python decaf_checker.py <decaf_source_file_name>

Lexer: decaf_lexer.py – scanner specification file built with PLY/lex. If Lexer thinks the program syntax is invalid, it will print "LEXER: SYNTAX ERROR".

Parser: decaf_parser.py – parser specification file built with PLY/yacc. If Parser thinks the program syntax is invalid, it will print "PARSER: SYNTAX ERROR".

AST: decaf_ast.py – table and class definitions for Decaf's AST. If AST thinks the program have same class, method, field, variable, it will print "Error".

Type checker: decaf_typecheck.py – Definitions for evaluating type constraints and name resolution. If there is a type error, it will print "Type Error".

Main: decaf_checker.py – containing the main python function to put together the lexer and parser, take the input from the Decaf program file, etc., and perform syntax checking. If the syntax of the program is valid, It will print "Yes".