#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
import sys
from decaf_lexer import *
from decaf_ast import *

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
    '''program : program class_decl
               | empty'''
    if(len(p)==3):
        p[0]=p[1]
        p[0].append(p[2])
    else:
        p[0]=[]

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID LBRACE class_body_decls RBRACE
                  | CLASS ID LBRACE class_body_decls RBRACE'''
    if(len(p)==6):
        p[0] = Class(p[2],None,p[4], p.lineno(2))
    else:
        p[0] = Class(p[2],p[4],p[6], p.lineno(2))

def p_class_body_decls(p):
    '''class_body_decls : class_body_decls class_body_decl
                        | class_body_decl'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]
        p[0].append(p[2])
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
    p[0]=p[1]

def p_field_decl(p):
    'field_decl : modifier var_decl'
    p[0] = Field(p[1], p[2])

def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    if(len(p)==3):
        p[0]=[p[1],'static']
    else:
        if(p[1]=='static'):
            p[0]=[None,p[1]]
        else:
            p[0]=[p[1],'non-static']

def p_var_decl(p):
    'var_decl : type variables SEMICOLON'
    Variable.var_type(p[1], p[2], p.lineno(3))
    p[0]=p[2]
                    
def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | ID'''
    p[0] = Type(p[1])

def p_variables(p):
    '''variables : variable
                 | variables COMMA variable'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]
        p[0].append(p[3])
                 
def p_variable(p):
    'variable : ID'
    p[0]=Variable(p[1], p.lineno(1))
    
def p_method_decl(p):
    '''method_decl : modifier type ID LPAREN formals RPAREN block
                   | modifier VOID ID LPAREN formals RPAREN block
                   | modifier type ID LPAREN RPAREN block
                   | modifier VOID ID LPAREN RPAREN block'''
    if (len(p) == 8):
        p[0] = Method(p[1],p[2],p[3],p[5],p[7], p.lineno(3))
    else:
        p[0] = Method(p[1],p[2],p[3],None,p[6], p.lineno(3))
                   
def p_constructor_decl(p):
    '''constructor_decl : modifier ID LPAREN formals RPAREN block
                        | modifier ID LPAREN RPAREN block'''
    if(len(p)==7):
        p[0] = Constructor(p[1],p[2],p[4],p[6], p.lineno(3))
    else:
        p[0] = Constructor(p[1],p[2],None,p[5], p.lineno(3))
                        
def p_formals(p):
    '''formals : formal_param
               | formals COMMA formal_param'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]
        p[0].append(p[3])
               
def p_formal_param(p):
    'formal_param : type variable'
    p[2].type=p[1]
    p[0]=p[2]
    
def p_block(p):
    'block : LBRACE stmts RBRACE'
    p[0]=p[2]

def p_stmts(p):
    '''stmts : stmts stmt
             | empty'''
    if(len(p)==3):
        p[0]=p[1]
        p[0].append(p[2])
    else:
        p[0]=[]
            
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
            | SEMICOLON'''
    stmt=Statement()
    if(p[1]=='if'):
        if(len(p)==8):
            Statement.if_stmt(stmt, p[3], p[5], p[7], p.lineno(1))
        else:
            Statement.if_stmt(stmt, p[3], p[5], None, p.lineno(1))
    elif(p[1]=='while'):
        Statement.while_stmt(stmt, p[3], p[5], p.lineno(1))
    elif(p[1]=='for'):
        if(len(p)==10):
            Statement.for_stmt(stmt, p[3], p[5], p[7], p[9], p.lineno(1))
        elif(len(p)==9):
            if(p[3]==';'):
                Statement.for_stmt(stmt, None, p[4], p[6], p[8], p.lineno(1))
            elif(p[6]==';'):
                Statement.for_stmt(stmt, p[3], p[5], None, p[8], p.lineno(1))
            else:
                Statement.for_stmt(stmt, p[3], None, p[6], p[8], p.lineno(1))
        elif(len(p)==8):
            if(p[3]!=';'):
                Statement.for_stmt(stmt, p[3], None, None, p[7], p.lineno(1))
            elif(p[4]!=';'):
                Statement.for_stmt(stmt, None, p[4], None, p[7], p.lineno(1))
            else:
                Statement.for_stmt(stmt, None, None, p[5], p[7], p.lineno(1))
        else:
            Statement.for_stmt(stmt, None, None, None, p[6], p.lineno(1))
    elif(p[1]=='return'):
        if(len(p)==4):
            Statement.return_stmt(stmt, p[2], p.lineno(1))
        else:
            Statement.return_stmt(stmt, None, p.lineno(1))
    elif(len(p)==3):
        if(p[1]=='break'):
            Statement.break_stmt(stmt, p.lineno(1))
        elif(p[1]=='continue'):
            Statement.continue_stmt(stmt, p.lineno(1))
        else:
            Statement.expr_stmt(stmt, p[1], p.lineno(2))
    elif(p[1]==';'):
        Statement.skip_stmt(stmt, p.lineno(1))
    else:
        p[0] = Statement.block_stmt(stmt, p[1], p.lineno(1))
    p[0] = stmt

def p_stmt_var_decl(p):
    'stmt : var_decl'
    stmt=Expression()
    Expression.var_expression(stmt, p[1])
    p[0]=stmt
    
def p_literal_int(p):
    'literal : INTCONST'
    literal=Expression()
    Expression.constant_expression(literal, 'int', p[1], p.lineno(1))
    p[0]=literal
def p_literal_float(p):
    'literal : FLOATCONST'
    literal=Expression()
    Expression.constant_expression(literal, 'float', p[1], p.lineno(1))
    p[0]=literal
def p_literal_string(p):
    'literal : STRINGCONST'
    literal=Expression()
    Expression.constant_expression(literal, 'string', p[1], p.lineno(1))
    p[0]=literal
def p_literal(p):
    '''literal : NULL
               | TRUE
               | FALSE'''
    literal=Expression()
    if(p[1]=='null'):
        Expression.constant_expression(literal, 'null', p[1], p.lineno(1))   
    else:
        Expression.constant_expression(literal, 'boolean', p[1], p.lineno(1)) 
    p[0]=literal

def p_primary(p):
    '''primary : literal
               | THIS
               | SUPER
               | LPAREN expr RPAREN
               | NEW ID LPAREN arguments RPAREN
               | NEW ID LPAREN RPAREN
               | lhs
               | method_invocation'''
    if(p[1]=='new'):
        expr=Expression()
        if(len(p)==6):
            Expression.new_object_expression(expr, p[2], p[4], p.lineno(1))
        else:
            Expression.new_object_expression(expr, p[2], None, p.lineno(1))
        p[0]=expr
    elif(p[1]=='this'):
        expr=Expression()
        Expression.this_expression(expr, p.lineno(1))
        p[0]=expr
    elif(p[1]=='super'):
        expr=Expression()
        Expression.super_expression(expr, p.lineno(1))
        p[0]=expr
    elif(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[2]

def p_arguments(p):
    '''arguments : expr
                 | arguments COMMA expr'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]
        p[0].append(p[3])
            
def p_lhs(p):
    'lhs : field_access'
    p[0]=p[1]

def p_field_access(p):
    '''field_access : primary DOT ID
                    | ID'''
    expr=Expression()
    if(len(p)==4):
        Expression.field_access_expression(expr, p[1], p[3], p.lineno(2))
    else:
        Expression.field_access_expression(expr, None, p[1], p.lineno(1))
    p[0]=expr

def p_method_invocation(p):
    '''method_invocation : field_access LPAREN arguments RPAREN
                         | field_access LPAREN RPAREN'''
    expr=Expression()
    if(len(p)==5):
        Expression.method_call_expression(expr, p[1], p[3], p.lineno(2))
    else:
        Expression.method_call_expression(expr, p[1], None, p.lineno(2))
    p[0]=expr

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
    if(p[1]=='-' or p[1]=='+' or p[1]=='!'):
        expr=Expression()
        Expression.unary_expression(expr, p[1], p[2], p.lineno(1))
        p[0]=expr
    elif(len(p)==4):
        expr=Expression()
        Expression.binary_expression(expr, p[1], p[2], p[3], p.lineno(2))
        p[0]=expr
    else:
        p[0]=p[1]

def p_assign(p):
    '''assign : lhs EQUAL expr
              | lhs PLUSPLUS
              | PLUSPLUS lhs
              | lhs MINUSMINUS
              | MINUSMINUS lhs'''
    expr=Expression()
    if(len(p)==4):
        Expression.assign_expression(expr, p[1], p[3], p.lineno(2))
    elif(p[1]=='++'):
        Expression.auto_expression(expr, p[2], 'auto-increment', 'pre', p.lineno(1))
    elif(p[1]=='--'):
        Expression.auto_expression(expr, p[2], 'auto-decrement', 'pre', p.lineno(1))
    elif(p[2]=='++'):
        Expression.auto_expression(expr, p[1], 'auto-increment', 'post', p.lineno(2))
    else:
        Expression.auto_expression(expr, p[1], 'auto-decrement', 'post', p.lineno(2))
    p[0]=expr

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    p[0]=p[1]

def p_empty(p):
    'empty :'
    p[0]=None

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