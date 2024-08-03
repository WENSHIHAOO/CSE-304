#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
import sys
reserved={
    'boolean' : 'BOOLEAN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'class' : 'CLASS',
    'else' : 'ELSE',
    'extends' : 'EXTENDS',
    'false' : 'FALSE',
    'float' : 'FLOAT',
    'for' : 'FOR',
    'if' : 'IF',
    'int' : 'INT',
    'new' : 'NEW',
    'null' : 'NULL',
    'private' : 'PRIVATE',
    'public' : 'PUBLIC',
    'return' : 'RETURN',
    'static' : 'STATIC',
    'super' : 'SUPER',
    'this' : 'THIS',
    'true' : 'TRUE',
    'void' : 'VOID',
    'while' : 'WHILE'
}
tokens = [ 
    # Boolean && || == != < > <= >= !
    'AND', 'OR', 'EQUALEQUAL', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'NOT', 
    # Assignment = ++ --
    'EQUAL', 'PLUSPLUS', 'MINUSMINUS',
    # Arithmetic + - * /
    'PLUS', 'MINUS', 'MULT', 'DIV',
    # Symbols ( ) { } ; , .
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA', 'DOT',
    # Identifier and Constant
    'ID', 'FLOATCONST', 'INTCONST', 'STRINGCONST'] + list(reserved.values())
# Boolean && || == != < > <= >= !
t_AND  = r'&&'
t_OR = r'\|\|'
t_EQUALEQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_NOT = r'!'
# Assignment = ++ --
t_EQUAL = r'='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'
# Arithmetic + - * /
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
# Symbols ( ) { } ; , .
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT= r'\.'
# Identifier and Constant
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
def t_FLOATCONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)    
    return t
def t_STRINGCONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t
# Comment \\ \* *\
def t_COMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    pass
def t_MULTILINECOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")
    pass
# From TT_lexer
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
def t_error(t):
    print()
    last_line = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    current_line = t.lexer.lexdata.find('\n', t.lexpos)
    if last_line < 0:
        last_line = 0
    print("LEXER: Syntax Error: Illegal Character '%s', at line %d, column %d" %(t.value[0], t.lineno, t.lexpos - last_line))
    print("CONTEXT: " + t.lexer.lexdata[last_line+1:current_line])
    print()
    sys.exit()