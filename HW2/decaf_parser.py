#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
import sys
from decaf_lexer import *

precedence = (# lowest precedence
    ('right', 'EQUAL'),                 # =
    ('left', 'OR'),                     # ||
    ('left', 'AND'),                    # &&
    ('left', 'EQUALEQUAL', 'NOTEQUAL'), # == !=
    ('nonassoc', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'),  # Nonassociative operators < > <= >=
    ('left', 'PLUS', 'MINUS'),          # + -
    ('left', 'MULT', 'DIV'),            # * /
    ('right', 'NOT'),                   # !
    ('right', 'UMINUS', 'UPLUS'),       # Unary minus operator
 )# highest precedence

def p_program(p):
    '''program : class_decl program
               | empty'''
    pass

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID LBRACE class_body_decls RBRACE
                  | CLASS ID LBRACE class_body_decls RBRACE'''
    pass

def p_class_body_decls(p):
    '''class_body_decls : class_body_decl class_body_decls
                        | class_body_decl'''
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
    pass

def p_field_decl(p):
    'field_decl : modifier var_decl'
    pass

def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    pass

def p_var_decl(p):
    'var_decl : type variables SEMICOLON'
    pass
                    
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | ID'''
    pass

def p_variables(p):
    '''variables : variable
                 | variable COMMA variables'''
    pass
                 
def p_variable(p):
    'variable : ID'
    pass
    
def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN formals RPAREN block
                   | modifier VOID ID LPAREN formals RPAREN block
                   | modifier type ID LPAREN RPAREN block
                   | modifier VOID ID LPAREN RPAREN block'''
    pass
                   
def p_constructor_decl(p):
    '''constructor_decl : modifier ID LPAREN formals RPAREN block
                        | modifier ID LPAREN RPAREN block'''
    pass
                        
def p_formals(p):
    '''formals : formal_param
               | formal_param COMMA formals'''
    pass
               
def p_formal_param(p):
    'formal_param : type variable'
    pass
    
def p_block(p):
    'block : LBRACE stmts RBRACE'
    pass

def p_stmts(p):
    '''stmts : stmt stmts
             | empty'''
    pass

def p_stmt(p):
    '''stmt : IF LPAREN expr RPAREN stmt ELSE stmt
            | IF LPAREN expr RPAREN stmt
            | WHILE LPAREN expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON RPAREN stmt
            | FOR LPAREN stmt_expr SEMICOLON SEMICOLON RPAREN stmt
            | FOR LPAREN SEMICOLON expr SEMICOLON RPAREN stmt
            | FOR LPAREN SEMICOLON SEMICOLON stmt_expr RPAREN stmt
            | FOR LPAREN SEMICOLON SEMICOLON RPAREN stmt
            | RETURN expr SEMICOLON
            | RETURN SEMICOLON
            | stmt_expr SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block
            | var_decl
            | SEMICOLON'''
    pass

def p_literal(p):
    '''literal : INTCONST
               | FLOATCONST
               | STRINGCONST
               | NULL
               | TRUE
               | FALSE'''
    pass

def p_primary(p):
    '''primary : literal
               | THIS
               | SUPER
               | LPAREN expr RPAREN
               | NEW ID LPAREN arguments RPAREN
               | NEW ID LPAREN RPAREN
               | lhs
               | method_invocation'''
    pass

def p_arguments(p):
    '''arguments : expr
                 | expr COMMA arguments'''
    pass

def p_lhs(p):
    'lhs : field_access'
    pass

def p_field_access(p):
    '''field_access : primary DOT ID
                    | ID'''
    pass

def p_method_invocation(p):
    '''method_invocation : field_access LPAREN arguments RPAREN
                         | field_access LPAREN RPAREN'''
    pass

def p_expr(p):
    '''expr : primary
            | assign
            | expr PLUS expr
            | expr MINUS expr
            | expr MULT expr
            | expr DIV expr
            | expr AND expr
            | expr OR expr
            | expr EQUALEQUAL expr
            | expr NOTEQUAL expr
            | expr LESS expr
            | expr GREATER expr
            | expr LESSEQUAL expr
            | expr GREATEREQUAL expr
            | MINUS expr %prec UMINUS
            | PLUS expr %prec UPLUS
            | NOT expr'''
    pass

def p_assign(p):
    '''assign : lhs EQUAL expr
              | lhs PLUSPLUS
              | PLUSPLUS lhs
              | lhs MINUSMINUS
              | MINUSMINUS lhs'''
    pass

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print()
    if p:
        last_line = p.lexer.lexdata.rfind('\n', 0, p.lexpos)
        current_line = p.lexer.lexdata.find('\n', p.lexpos)
        if last_line < 0:
            last_line = 0
        print("PARSER: Syntax Error:  Token '%s', at line %d, column %d" %(p.value, p.lineno, p.lexpos - last_line))
        print("CONTEXT: " + p.lexer.lexdata[last_line+1:current_line])
    else:
        print("PARSER: Syntax Error at EOF")
    print()
    sys.exit()