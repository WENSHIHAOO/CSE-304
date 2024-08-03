#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
from decaf_ast import *

type_error=False
return_type=''
this=None
var_ref=[]
def check_frist_is_subtype(t1, t2):
    if(t1 == t2):
        return True
    elif(t1=='int' and t2=='float'):
        return True
    elif(t2 not in ['int', 'boolean', 'float', 'string', 'void', 'error', 'null']):
        if(t1 == 'null'):
            return True
        elif(t1 not in ['int', 'boolean', 'float', 'string', 'void', 'error', 'null']):
            s=check_super(t1)
            while(s != None):
                if(s == t2):
                    return True
                s=check_super(s)
    return False

def check_super(object):
    if(class_table[object.class_name].super_class_name == None):
        return None
    return class_table[class_table[object.class_name].super_class_name]

def check_program():
    global type_error
    print("Type_Check: Start\n")
    for Class in class_table.values():
        check_class(Class)
    if(type_error):
        sys.exit()
    print("Type_Check: End")
    return None

def check_class(object):
    global this
    this = object
    for constructor in object.class_constructors:
        check_constructor(constructor)
        
    for method in object.methods.values():
        check_method(method)
    return None

def check_constructor(object):
    global var_ref
    var_ref.append(object.constructor_parameters)
    var_ref.append(object.variable_table)
    for stmt in object.constructor_body:
        check_index(stmt)
    var_ref.pop()
    var_ref.pop()
    return None

def check_method(object):
    global var_ref
    var_ref.append(object.method_parameters)
    var_ref.append(object.variable_table)
    global return_type
    if(object.return_type == 'void'):
        return_type = object.return_type
    else:
        return_type = object.return_type.type
    for stmt in object.method_body:
        check_index(stmt)
    var_ref.pop()
    var_ref.pop()
    return None

def check_index(object):
    if(object == None):
        return 'null'
    
    elif(type(object) is str):
        return object
    
    elif(type(object) is list):
        for i in list:
            check_index(i)
        return None
       
    elif(type(object) is Variable):
        return check_index(object.type)
    
    elif(type(object) is Type):
        return object.type
        
    elif(type(object) is Statement):
        if(object.id=='if'):
            return check_Statement.check_if_stmt(object)
        elif(object.id=='while'):
            return check_Statement.check_while_stmt(object)
        elif(object.id=='for'):
            return check_Statement.check_for_stmt(object)
        elif(object.id=='return'):
            return check_Statement.check_return_stmt(object)
        elif(object.id=='expr'):
            return check_Statement.check_expr_stmt(object)
        elif(object.id=='block'):
            return check_Statement.check_block_stmt(object)
        elif(object.id=='break'):
            return None
        elif(object.id=='continue'):
            return None
        elif(object.id=='skip'):
            return None
        
    elif(type(object) is Expression):
        if(object.id=='constant'):
            return check_Expression.check_constant_expression(object)
        elif(object.id=='var'):
            return check_Expression.check_var_expression(object)
        elif(object.id=='unary'):
            return check_Expression.check_unary_expression(object)
        elif(object.id=='binary'):
            return check_Expression.check_binary_expression(object)
        elif(object.id=='assign'):
            return check_Expression.check_assign_expression(object)
        elif(object.id=='auto'):
            return check_Expression.check_auto_expression(object)
        elif(object.id=='field_access'):
            return check_Expression.check_field_access_expression(object)
        elif(object.id=='method_call'):
            return check_Expression.check_method_call_expression(object)
        elif(object.id=='new_object'):
            return check_Expression.check_new_object_expression(object)
        elif(object.id=='this'):
            return check_Expression.check_this_expression(object)
        elif(object.id=='super'):
            return check_Expression.check_super_expression(object)
        elif(object.id=='class_reference'):
            return check_Expression.check_class_reference_expression(object)
    print(object)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print('Error: check_index')
    sys.exit
        
class check_Statement(object):
    def check_if_stmt(stmt):
        if(not check_frist_is_subtype(check_index(stmt.condition), 'boolean')):
            print("Type Error: if_condition, at line %d" %(stmt.line))
            global type_error
            type_error=True
            
        global var_ref
        if(type(stmt.then_stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.then_stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    for var in s.variable_table:
                        stmt.check_var[var.variable_name]=var
                #
                check_index(s)
            var_ref.pop()
        else:
            check_index(stmt.then_stmt)
            
        stmt.check_var={}
        
        if(stmt.stmt != None):
            if(type(stmt.stmt) is list):
                var_ref.append(stmt.check_var)
                for s in stmt.stmt:
                    #
                    if(type(s) is Expression and s.id == 'var'):
                        for var in s.variable_table:
                            stmt.check_var[var.variable_name]=var
                    #
                    check_index(s)
                var_ref.pop()
            else:
                check_index(stmt.stmt)
        return None
    
    def check_while_stmt(stmt):
        global var_ref
        if(not check_frist_is_subtype(check_index(stmt.condition), 'boolean')):
            print("Type Error: while_condition, at line %d" %(stmt.line))
            global type_error
            type_error=True
            
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    for var in s.variable_table:
                        stmt.check_var[var.variable_name]=var
                #
                check_index(s)
            var_ref.pop()
        else:
            check_index(stmt.stmt)
        return None
    
    def check_for_stmt(stmt):
        global var_ref
        check_index(stmt.initializer)
        if(not check_frist_is_subtype(check_index(stmt.condition), 'boolean')):
            print("Type Error: for_condition, at line %d" %(stmt.line))
            global type_error
            type_error=True
        check_index(stmt.update)
        
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    for var in s.variable_table:
                        stmt.check_var[var.variable_name]=var
                #
                check_index(s)
            var_ref.pop()
        else:
            check_index(stmt.stmt)
        return None
    
    def check_return_stmt(stmt):
        error=False
        global return_type
        if(stmt.expr==None and return_type!='void'):
            error=True
        else:
            if(not check_frist_is_subtype(check_index(stmt.expr), return_type)):
                error=True
        if(error):
            print("Type Error: return, at line %d" %(stmt.line))
            global type_error
            type_error=True
            return 'error'
        return None
    
    def check_expr_stmt(stmt):
        global var_ref
        if(type(stmt.expr) is list):
            var_ref.append(stmt.check_var)
            for e in stmt.expr:
                #
                if(type(e) is Expression and e.id == 'var'):
                    for var in e.variable_table:
                        stmt.check_var[var.variable_name]=var
                #
                check_index(e)
            var_ref.pop()
        else:
            check_index(stmt.expr)
        return None
    
    def check_block_stmt(stmt):
        global var_ref
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    for var in s.variable_table:
                        stmt.check_var[var.variable_name]=var
                #
                check_index(s)
            var_ref.pop()
        else:
            check_index(stmt.stmt)
        return None
            
class check_Expression():
    def check_constant_expression(expr):
        expr.typecheck=expr.expression1
        return expr.expression1
    
    def check_var_expression(expr):
        expr.typecheck=expr.variable_table[0].type.type
        return expr.variable_table[0].type.type
    
    def check_unary_expression(expr):
        t=check_index(expr.expression1)
        if(expr.operator1=='!'):
            if(t=='boolean'):
                expr.typecheck='boolean'
                return 'boolean'
        else:
            if(t in ['int', 'float']):
                expr.typecheck=t
                return t
        print("Type Error: unary_expression, at line %d" %(expr.line))
        global type_error
        type_error=True
        expr.typecheck='error'
        return 'error'
    
    def check_binary_expression(expr):
        t1=check_index(expr.expression1)
        t2=check_index(expr.expression2)
        if(expr.operator1 in ['add', 'sub', 'mul', 'div']):
            if(t1==t2 and t2=='int'):
                expr.typecheck='int'
                return 'int'
            elif(t1 in ['int', 'float'] and t2 in ['int', 'float']):
                expr.typecheck='float'
                return 'float'
        elif(expr.operator1 in ['and', 'or']):
            if(t1==t2 and t2=='boolean'):
                expr.typecheck='boolean'
                return 'boolean'
        elif(expr.operator1 in ['lt', 'leq', 'gt', 'geq']):
            if(t1 in ['int', 'float'] and t2 in ['int', 'float']):
                expr.typecheck='boolean'
                return 'boolean'
        elif(expr.operator1 in ['eq', 'neq']):
            if(check_frist_is_subtype(t1, t2) or check_frist_is_subtype(t2, t1)):
                expr.typecheck='boolean'
                return 'boolean'
        print("Type Error: binary_expression, at line %d" %(expr.line))
        global type_error
        type_error=True
        expr.typecheck='error'
        return 'error'
    
    def check_assign_expression(expr):
        t1=check_index(expr.expression1)
        t2=check_index(expr.expression2)
        if(check_frist_is_subtype(t2, t1)):
            expr.operator1=t1
            expr.operator2=t2
            expr.typecheck=t2
            return t2
        print("Type Error: assign_expression, at line %d" %(expr.line))
        global type_error
        type_error=True
        expr.typecheck='error'
        return 'error'
    
    def check_auto_expression(expr):
        t=check_index(expr.expression1)
        if(t in ['int', 'float']):
            expr.typecheck=t
            return t
        print("Type Error: auto_expression, at line %d" %(expr.line))
        global type_error
        type_error=True
        expr.typecheck='error'
        return 'error'
    
    def check_field_access_expression(expr):
        global this
        global var_ref
        global type_error
        f=None
        #lhs
        if(expr.expression1==None):
            for array in reversed(var_ref):
                if expr.expression2 in array:
                    expr.typecheck=array[expr.expression2].type.type
                    return array[expr.expression2].type.type
            f=check_name_resolution(this, expr)
            expr.typecheck=f[1]
            return f[1]
        #p.x: z
        else:
            expression1=None
            if(expr.expression1.expression1==None):
                expression1=expr.expression1.expression2
                
                for array in reversed(var_ref):
                    if expression1 in array:
                        #'user'
                        f=check_name_resolution(class_table[array[expression1].type.type], expr)
                        if(type(f[0]) is Field): 
                            if(f[0].field_applicability=='static'):
                                print("Type Error: field_access_expression -> p=user(A) and z=static field, at line %d" %(expr.line))
                                type_error=True
                            if(f[0].field_visibility=='private'):
                                print("Type Error: field_access_expression -> field is private, at line %d" %(expr.line))
                                type_error=True
                        expr.typecheck=f[1]
                        return f[1]
                    
                if(expression1 == 'this'):
                    #'user'
                    f=check_name_resolution(this, expr)
                    if((type(f[0]) is Field)):
                        if(f[0].field_applicability=='static'):
                            print("Type Error: field_access_expression -> p=user(A) and z=static field, at line %d" %(expr.line))
                            type_error=True
                        if(f[0].field_visibility=='private'):
                            print("Type Error: field_access_expression -> field is private, at line %d" %(expr.line))
                            type_error=True
                    expr.typecheck=f[1]
                    return f[1]
                elif(expression1 == 'super'):
                    s=check_super(this)
                    if(s==None):
                        print()
                        print("Error: super==None, at line %d" %(expr.line))
                        print()
                        sys.exit()
                    else:
                        #'user'
                        f=check_name_resolution(s, expr)
                        if((type(f[0]) is Field)):
                            if(f[0].field_applicability=='static'):
                                print("Type Error: field_access_expression -> p=user(A) and z=static field, at line %d" %(expr.line))
                                type_error=True
                            if(f[0].field_visibility=='private'):
                                print("Type Error: field_access_expression -> field is private, at line %d" %(expr.line))
                                type_error=True
                        expr.typecheck=f[1]
                        return f[1]
                elif expression1 in class_table:
                    #'classliteral'
                    f=check_name_resolution(class_table[expression1], expr)
                    if(type(f[0]) is Field):
                        if(f[0].field_applicability=='non-static'):
                            print("Type Error: field_access_expression -> p=class-literal(A) and z=non-static field, at line %d" %(expr.line))
                            type_error=True
                        if(f[0].field_visibility=='private'):
                            print("Type Error: field_access_expression -> field is private, at line %d" %(expr.line))
                            type_error=True
                    expr.typecheck=f[1]
                    return f[1]
            else:
                expression1=check_index(expr.expression1)
                #'user'
                f=check_name_resolution(class_table[expression1], expr)
                if(type(f[0]) is Field): 
                    if(f[0].field_applicability=='static'):
                        print("Type Error: field_access_expression -> p=user(A) and z=static field, at line %d" %(expr.line))
                        type_error=True
                    if(f[0].field_visibility=='private'):
                        print("Type Error: field_access_expression -> field is private, at line %d" %(expr.line))
                        type_error=True
                expr.typecheck=f[1]
                return f[1]
    
    def check_method_call_expression(expr):
        global this
        global var_ref
        global type_error
        f=None
        #f(e_1, ..., e_n): h
        if(expr.expression1.expression1==None):
            f=check_name_resolution(this, expr)
            expr.typecheck=f[1]
            return f[1]
        ##p.f(e_1, ..., e_n): h
        else:
            p=None
            expression1=expr.expression1
            if(expression1.expression1.expression1==None):
                notFind=True
                for array in reversed(var_ref):
                    if expression1.expression1.expression2 in array:
                        #'user'
                        p=class_table[array[expression1.expression1.expression2].type.type]
                        notFind=False
                        f=check_name_resolution(p, expr)
                        if(f[0].method_applicability=='static'):
                            print("Type Error: method_call_expression -> p=user(A) and h=static method, at line %d" %(expr.line))
                            type_error=True
                        if(f[0].method_visibility=='private'):
                            print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                            type_error=True
                        expr.typecheck=f[1]
                        return f[1]
                if(notFind):
                    for field in this.fields:
                        for field_name in field.field_name:
                            if(field_name == expression1.expression1.expression2):
                                #'user'
                                p=class_table[field.type.type]
                                notFind=False
                                f=check_name_resolution(p, expr)
                                if(f[0].method_applicability=='static'):
                                    print("Type Error: method_call_expression -> p=user(A) and h=static method, at line %d" %(expr.line))
                                    type_error=True
                                if(f[0].method_visibility=='private'):
                                    print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                                    type_error=True
                                expr.typecheck=f[1]
                                return f[1]
                if(notFind):
                    if(expression1.expression1.expression2 == 'this'):
                        #'user'
                        f=check_name_resolution(this, expr)
                        if(f[0].method_applicability=='static'):
                            print("Type Error: method_call_expression -> p=user(A) and h=static method, at line %d" %(expr.line))
                            type_error=True
                        if(f[0].method_visibility=='private'):
                            print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                            type_error=True
                        expr.typecheck=f[1]
                        return f[1]
                    elif(expression1.expression1.expression2 == 'super'):
                        s=check_super(this)
                        if(s==None):
                            print()
                            print("Error: super==None, at line %d" %(expr.line))
                            print()
                            sys.exit()
                        else:
                            #'user'
                            f=check_name_resolution(s, expr)
                            if(f[0].method_applicability=='static'):
                                print("Type Error: method_call_expression -> p=user(A) and h=static method, at line %d" %(expr.line))
                                type_error=True
                            if(f[0].method_visibility=='private'):
                                print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                                type_error=True
                            expr.typecheck=f[1]
                            return f[1]
                    elif expression1.expression1.expression2 in class_table:
                        #'classliteral'
                        p=class_table[expression1.expression1.expression2]
                        notFind=False
                        f=check_name_resolution(p, expr)
                        if(f[0].method_applicability=='non-static'):
                            print("Type Error: method_call_expression -> p=class-literal(A) and h=non-static method, at line %d" %(expr.line))
                            type_error=True
                        if(f[0].method_visibility=='private'):
                            print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                            type_error=True
                        expr.typecheck=f[1]
                        return f[1]
                print()
                print()
                print("Variables Error: method_call_expression -> variables not uninitialized.")
                print("Variable Name: '%s', at line %d" %(expression1.expression1.expression2, expr.line))
                print()
                sys.exit()
            else:
                #'user'
                p=class_table[check_index(expression1.expression1)]
                f=check_name_resolution(p, expr)
                if(f[0].method_applicability=='static'):
                    print("Type Error: method_call_expression -> p=user(A) and h=static method, at line %d" %(expr.line))
                    type_error=True
                if(f[0].method_visibility=='private'):
                    print("Type Error: method_call_expression -> method is private, at line %d" %(expr.line))
                    type_error=True
                expr.typecheck=f[1]
                return f[1]

    def check_new_object_expression(expr):
        global this
        #new A(e_1, ..., e_n)
        if expr.expression1 in class_table:
            f=check_name_resolution(class_table[expr.expression1], expr)
            if(f[0].constructor_visibility=='private' and expr.expression1 != this.class_name):
                print("Type Error: new_object_expression -> constructor is private, at line %d" %(expr.line))
                global type_error
                type_error=True
            expr.typecheck=f[1]
            return f[1]
        else:
            print()
            print("Class Error: new_object_expression -> No such class.")
            print("Class Name: '%s', at line %d" %(expr.expression1, expr.line))
            print()
            sys.exit()
        
    def check_this_expression(expr):
        global this
        expr.typecheck=this.class_name
        return this.class_name
        
    def check_super_expression(expr):
        global this
        super_name=check_super(this).class_name
        expr.typecheck=super_name
        return super_name
        
    def check_class_reference_expression(expr):
        a=check_name_resolution(expr)
        if(a != None):
            expr.typecheck=a[1]
            return a[1]
        print("Type Error: new_object_expression, at line %d" %(expr.line))
        global type_error
        type_error=True
        return 'error'
        
def check_name_resolution(p, expr):
    global return_type
    if(expr.id=='field_access'):
        while(p != None):
            for field in p.fields:
                for field_name in field.field_name:
                    if(field_name == expr.expression2):
                        expr.field_id=field.field_id
                        return [field, field.type.type]
            p=check_super(p)
        print()
        print("Field Error: name_resolution_field -> No such Field.")
        print("Field Name: '%s', at line %d" %(expr.expression2, expr.line))
        print()
        sys.exit()
    elif(expr.id=='method_call'):
        name=expr.expression1.expression2
        if(expr.arguments != None):
            for e in expr.arguments:
                name+=check_index(e)
                
        while(p != None):
            for method_name in p.methods:
                if method_name == name:
                    expr.method_id=p.methods[method_name].method_id
                    return [p.methods[method_name], check_index(p.methods[method_name].return_type)]
            p=check_super(p)
        print()
        print("Method Error: name_resolution_method -> No such method.")
        print("Method Name: '%s', at line %d" %(expr.expression1.expression2, expr.line))
        print()
        sys.exit()
    elif(expr.id=='new_object'):
        for constructor in p.class_constructors:
            fomal=True
            if(expr.arguments != None):
                if(len(constructor.constructor_parameters) == len(expr.arguments)):
                    for val1, val2 in zip(constructor.constructor_parameters.values(), expr.arguments):
                        if(not check_frist_is_subtype(check_index(val2), val1.type.type)):
                            fomal=False
                            break
                else:
                    fomal=False
            elif(len(constructor.constructor_parameters)!=0):
                fomal=False
            if(fomal):
                expr.constructor_id=constructor.constructor_id
                return [constructor, p.class_name]
        print()
        print("Constructor Error: name_resolution_constructor -> No such constructor.")
        print("Constructor Name: '%s', at line %d" %(expr.expression1, expr.line))
        print()
        sys.exit()