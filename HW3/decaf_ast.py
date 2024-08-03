#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
import sys

constructor_id=1
method_id=1
field_id = 1
class_table={}
var_class={}
var_array_ref=[]
var_array_ref.append(var_class)
class Class(object):
    def __init__(self, ID, EXTENDS_ID, class_body_decls):
        self.class_name=ID
        self.super_class_name=EXTENDS_ID
        self.class_constructors=[]
        self.methods={}
        self.fields=[]
        self.fields_check={}
        self.var_method={}
        self.var_field={}
        for class_body_decl in class_body_decls:
            if type(class_body_decl) is Constructor:
                self.class_constructors.append(class_body_decl)
            elif type(class_body_decl) is Method:
                method_name=class_body_decl.method_name
                for parameter in class_body_decl.method_parameters.values():
                    method_name+=parameter.type.type
                if(method_name in self.methods):
                    print()
                    print("Method Error: two methods with the same name and same type signatures.")
                    print("Class Name: "+self.class_name)
                    print("Method Name: "+class_body_decl.method_name)
                    print()
                    sys.exit()
                class_body_decl.containing_class=ID
                self.methods[method_name]=class_body_decl
                self.var_method[class_body_decl.method_name]=Variable(method_name)
                #self.var_method[method_name]=Variable(method_name), keep it
            elif type(class_body_decl) is Field:
                class_body_decl.containing_class=ID
                for var in class_body_decl.field_name:
                    if(var+ID in self.fields_check):
                        print()
                        print("Fields Error: two fields declared in the same class have same names")
                        print("Class Name: "+self.class_name)
                        print("Fields Name: "+var)
                        print()
                        sys.exit()
                    self.fields_check[var+ID]=var
                self.fields.append(class_body_decl)
                self.var_field[var]=Variable(var)
        global class_table
        if(self.class_name in class_table):
            print()
            print("Class Error: two classes with the same name.")
            print("Class Name: "+self.class_name)
            print()
            sys.exit()
        class_table[self.class_name]=self
        var_class[ID]=Variable(ID)
        
    def __str__(self):
        var_array_ref.append(self.var_method)
        var_array_ref.append(self.var_field)
        print("Class Name:", self.class_name)
        if(self.super_class_name==None):
            print("Superclass Name:\n")
        else:
            print("Superclass Name:", self.super_class_name,'\n')
            
        if(len(self.fields)==0):
            print("Fields:\n")
        else:
            print("Fields:")
        for i, field in enumerate(self.fields):
            if i == len(self.fields) - 1:
                print(field)
            else:
                print(field, end='')
                
        if(len(self.class_constructors)==0):
            print("Constructors:\n")
        else:
            print("Constructors:")
        for i, constructor in enumerate(self.class_constructors):
            if i == len(self.class_constructors) - 1:
                print(constructor)
            else:
                print(constructor, end='')
                
        print("Methods:")
        for i, method in enumerate(self.methods.values()):
            if i == len(self.methods) - 1:
                print(method)
            else:
                print(method, end='')
        var_array_ref.pop()
        var_array_ref.pop()
        return ''
                
class Constructor(object):
    def __init__(self, modifier, ID, formals, block):
        global constructor_id
        self.constructor_id=constructor_id
        constructor_id+=1
        self.constructor_visibility=modifier[0] #public/private
        
        variable_id=1
        self.constructor_parameters={}
        if(formals != None):
            for formal_param in formals:
                if type(formal_param) is Variable:
                    formal_param.variable_kind='formal'
                    formal_param.variable_id=variable_id
                    variable_id+=1
                    self.constructor_parameters[formal_param.variable_name]=formal_param
        
        self.variable_table={}
        for stmt in block:
            if(type(stmt) is Expression):
                for var in stmt.variable_table:
                    if(var.variable_name in self.constructor_parameters
                       or var.variable_name in self.variable_table):
                        print()
                        print("Constructor variables Error: two variables in the same scopes have same name.")
                        print("Constructor Name: "+ID)
                        print("Variable Name: "+var.variable_name)
                        print()
                        sys.exit()
                    var.variable_id=variable_id
                    variable_id+=1
                    self.variable_table[var.variable_name]=var
        self.constructor_body=block
        
    def __str__(self):
        var_array_ref.append(self.constructor_parameters)
        var_array_ref.append(self.variable_table)
        print("CONSTRUCTOR:", self.constructor_id,',', self.constructor_visibility)
        print("Constructor Parameters:", end='')
        parameters=''
        for parameter in self.constructor_parameters.values():
            parameters+=(', '+str(parameter.variable_id))
        print(parameters[1:])
        print("Variable Table:")
        for parameter in self.constructor_parameters.values():
            print(parameter)
        for variable in self.variable_table.values():
            print(variable)
        print("Constructor Body:")
        print("Block([")
        first=True
        for stmt in self.constructor_body:
            if(stmt.id=='var'):
                continue
            if(first):
                first=False
                stmt.__str__(var_array_ref)
            else:
                print(', ',end='')
                stmt.__str__(var_array_ref)
            print()
        print("])")
        var_array_ref.pop()
        var_array_ref.pop()
        return ''
    
class Method(object):
    def __init__(self, modifier, type_, ID, formals, block):
        self.method_name=ID
        global method_id
        self.method_id=method_id
        method_id+=1
        self.containing_class=None
        self.method_visibility=modifier[0] #public/private
        self.method_applicability=modifier[1]
        
        variable_id=1
        self.method_parameters={}
        if(formals != None):
            for formal_param in formals:
                if type(formal_param) is Variable:
                    formal_param.variable_kind='formal'
                    formal_param.variable_id=variable_id
                    variable_id+=1
                    self.method_parameters[formal_param.variable_name]=formal_param
            
        self.return_type=type_
        
        self.variable_table={}
        for stmt in block:
            if(type(stmt) is Expression):
                for var in stmt.variable_table:
                    if(var.variable_name in self.method_parameters
                       or var.variable_name in self.variable_table):
                        print()
                        print("Method variables Error: two variables in the same block have same name.")
                        print("Method Name: "+self.method_name)
                        print("Variable Name: "+var.variable_name)
                        print()
                        sys.exit()
                    var.variable_id=variable_id
                    variable_id+=1
                    self.variable_table[var.variable_name]=var
        self.method_body=block
        
    def __str__(self):
        var_array_ref.append(self.method_parameters)
        var_array_ref.append(self.variable_table)
        print("METHOD:", self.method_id,',', self.method_name,',', self.containing_class,',', 
              self.method_visibility,',', self.method_applicability,',', self.return_type)
        print("Method Parameters:", end='')
        parameters=''
        for parameter in self.method_parameters.values():
            parameters+=(', '+str(parameter.variable_id))
        print(parameters[1:])
        print("Variable Table:")
        for parameter in self.method_parameters.values():
            print(parameter)
        for variable in self.variable_table.values():
            print(variable)
        print("Method Body:")
        print("Block([")
        first=True
        for stmt in self.method_body:
            if(stmt.id=='var'):
                continue
            if(first):
                first=False
                stmt.__str__(var_array_ref)
            else:
                print(', ',end='')
                stmt.__str__(var_array_ref)
            print()
        print("])")
        var_array_ref.pop()
        var_array_ref.pop()
        return ''

class Field(object):
    def __init__(self, modifier, var_decl):
        self.field_name=[]
        variable_id=1
        for variable in var_decl:
            if type(variable) is Variable:
                variable.variable_id=variable_id
                variable_id+=1
                self.field_name.append(variable.variable_name)
                
        global field_id
        self.field_id=field_id
        field_id+=1
        self.containing_class=None
        self.field_visibility=modifier[0]
        self.field_applicability=modifier[1]
        self.type=var_decl[0].type
        
    def __str__(self):
        print("FIELD", self.field_id,',', self.field_name,',', self.containing_class,',', 
              self.field_visibility,',', self.field_applicability,',', self.type)
        return ''
    
class Variable(object):
    def __init__(self, ID):
        self.variable_name=ID
        self.variable_id=0
        self.variable_kind=None
        self.type=None
        
    def var_type(type_, variables):
        for variable in variables:
            if type(variable) is Variable:
                variable.type=type_
                
    def __str__(self):
        print("VARIABLE", self.variable_id,',', self.variable_name,',',
                self.variable_kind,',', self.type, end='')
        return ''
            
class Type(object):
    def __init__(self, type_name):
        self.type=type_name
        
    def __str__(self):
        if(self.type=='int' or self.type=='float' or self.type=='boolean'):
            print(self.type, end='')
        else:
            print('user('+self.type+')', end='')
        return ''
        
class Statement(object):
    def __init__(self):
        self.id=None
        self.condition=None
        self.then_stmt=None
        self.stmt=None
        self.initializer=None
        self.update=None
        self.expr=None
        self.check_var={}
    def if_stmt(self, expr, if_stmt, else_stmt):
        self.id='if'
        self.condition=expr
        self.then_stmt=if_stmt
        self.stmt=else_stmt
    def while_stmt(self, expr, while_stmt):
        self.id='while'
        self.condition=expr
        self.stmt=while_stmt
    def for_stmt(self, stmt_expr, expr, update_stmt_expr, stmt):
        self.id='for'
        self.initializer=stmt_expr
        self.condition=expr
        self.update=update_stmt_expr
        self.stmt=stmt
    def return_stmt(self, expr):
        self.id='return'
        self.expr=expr
    def expr_stmt(self, stmt_expr):
        self.id='expr'
        self.expr=stmt_expr
    def block_stmt(self, block):
        self.id='block'
        self.stmt=block
    def break_stmt(self):
        self.id='break'
    def continue_stmt(self):
        self.id='continue'
    def skip_stmt(self):
        self.id='skip'
    def check_var_array(self, vars):
        for var in vars.variable_table:
            if(var.variable_name in self.check_var):
                print()
                print("\nVariables Error: two variables in the same scopes have same name.")
                print("Scope Name: "+self.id)
                print("Variable Name: "+var.variable_name)
                print()
                sys.exit()
            self.check_var[var.variable_name]=var
            var.variable_kind='local'
        
    def __str__(self, var_array_ref):
        if(self.id=='if'):
            print("If( ",end='')
            self.condition.__str__(var_array_ref),
            print(" ){ ",end='')
            if(type(self.then_stmt) is list):
                var_array_ref.append(self.check_var)
                for i, s in enumerate(self.then_stmt):
                    #
                    if(type(s) is Expression):
                        if(s.id == 'var'):
                            self.check_var_array(s)
                    #
                    if i == len(self.then_stmt) - 1:
                        s.__str__(var_array_ref)
                    else:
                        s.__str__(var_array_ref)
                        print(' , ',end='')
                var_array_ref.pop()
            else:
                self.then_stmt.__str__(var_array_ref)
            print(" }",end='')
            self.check_var={}
            
            if(self.stmt != None):
                print("Else{ ",end='')
                if(type(self.stmt) is list):
                    var_array_ref.append(self.check_var)
                    for i, s in enumerate(self.stmt):
                        #
                        if(type(s) is Expression):
                            if(s.id == 'var'):
                                self.check_var_array(s)
                        #
                        if i == len(self.stmt) - 1:
                            s.__str__(var_array_ref)
                        else:
                            s.__str__(var_array_ref)
                            print(' , ',end='')
                    var_array_ref.pop()
                else:
                    self.stmt.__str__(var_array_ref)
                print(" }",end='')
        elif(self.id=='while'):
            print("While( ",end='')
            self.condition.__str__(var_array_ref)
            print(" ){ ",end='')
            if(type(self.stmt) is list):
                var_array_ref.append(self.check_var)
                for i, s in enumerate(self.stmt):
                    #
                    if(type(s) is Expression):
                        if(s.id == 'var'):
                            self.check_var_array(s)
                    #
                    if i == len(self.stmt) - 1:
                        s.__str__(var_array_ref)
                    else:
                        s.__str__(var_array_ref)
                        print(' , ',end='')
                var_array_ref.pop()
            else:
                self.stmt.__str__(var_array_ref)
            print(" }",end='')
        elif(self.id=='for'):
            print("For( ",end='')
            if(self.initializer != None):
                self.initializer.__str__(var_array_ref)
            print(" ; ",end='')
            if(self.condition != None):
                self.condition.__str__(var_array_ref)
            print(" ; ",end='')
            if(self.update != None):
                self.update.__str__(var_array_ref)
            print(" ){ ",end='')
            if(type(self.stmt) is list):
                var_array_ref.append(self.check_var)
                for i, s in enumerate(self.stmt):
                    #
                    if(type(s) is Expression):
                        if(s.id == 'var'):
                            self.check_var_array(s)
                    #
                    if i == len(self.stmt) - 1:
                        s.__str__(var_array_ref)
                    else:
                        s.__str__(var_array_ref)
                        print(' , ',end='')
                var_array_ref.pop()
            else:
                self.stmt.__str__(var_array_ref)
            print(" }",end='')
        elif(self.id=='return'):
            print("Return( ",end='')
            self.expr.__str__(var_array_ref)
            print(" )",end='')
        elif(self.id=='expr'):
            print("Expr( ",end='')
            if(type(self.expr) is list):
                var_array_ref.append(self.check_var)
                for i, e in enumerate(self.expr):
                    #
                    if(type(e) is Expression):
                        if(e.id == 'var'):
                            self.check_var_array(e)
                    #
                    if i == len(self.expr) - 1:
                        e.__str__(var_array_ref)
                    else:
                        e.__str__(var_array_ref)
                        print(' , ',end='')
                var_array_ref.pop()
            else:
                self.expr.__str__(var_array_ref)
            print(" )",end='')
        elif(self.id=='block'):
            if(type(self.stmt) is list):
                var_array_ref.append(self.check_var)
                for i, s in enumerate(self.stmt):
                    #
                    if(type(s) is Expression):
                        if(s.id == 'var'):
                            self.check_var_array(s)
                    #
                    if i == len(self.stmt) - 1:
                        s.__str__(var_array_ref)
                    else:
                        s.__str__(var_array_ref)
                        print(' , ',end='')
                var_array_ref.pop()
            else:
                self.stmt.__str__(var_array_ref)
        elif(self.id=='break'):
            print("Break",end='')
        elif(self.id=='continue'):
            print("Continue",end='')
        else:
            print("Skip",end='')
        return ''
        
class Expression(object):
    def __init__(self):
        self.id=None
        self.expression1=None
        self.expression2=None
        self.variable_table=None
        self.operator1=None
        self.operator2=None
        self.arguments=None
    def constant_expression(self, constant, value):
        self.id='constant'
        self.expression1=constant
        self.expression2=value
    def var_expression(self, reference_id):
        self.id='var'
        self.variable_table=reference_id
        for var in self.variable_table:
            var.variable_kind='local'
    def unary_expression(self, unary_operator, expr):
        self.id='unary'
        self.operator1=unary_operator
        self.expression1=expr
    def binary_expression(self, expr1, binary_operator, expr2):
        self.id='binary'
        self.expression1=expr1
        if(binary_operator=='+'):
            self.operator1='add'
        elif(binary_operator=='-'):
            self.operator1='sub'
        elif(binary_operator=='*'):
            self.operator1='mul'
        elif(binary_operator=='/'):
            self.operator1='div'
        elif(binary_operator=='&&'):
            self.operator1='and'
        elif(binary_operator=='||'):
            self.operator1='or'
        elif(binary_operator=='=='):
            self.operator1='eq'
        elif(binary_operator=='!='):
            self.operator1='neq'
        elif(binary_operator=='<'):
            self.operator1='lt'
        elif(binary_operator=='<='):
            self.operator1='leq'
        elif(binary_operator=='>'):
            self.operator1='gt'
        elif(binary_operator=='>='):
            self.operator1='geq'
        self.expression2=expr2
    def assign_expression(self, lhs, expr):
        self.id='assign'
        self.expression1=lhs
        self.expression2=expr
    def auto_expression(self, lhs, increment_decrement, post_pre):
        self.id='auto'
        self.expression1=lhs
        self.operator1=increment_decrement
        self.operator2=post_pre
    def field_access_expression(self, base, field):
        self.id='field_access'
        self.expression1=base
        self.expression2=field
    def method_call_expression(self, field_access, arguments):
        self.id='method_call'
        self.expression1=field_access.expression1 #field_access
        self.expression2=field_access.expression2 #field
        self.arguments=arguments
    def new_object_expression(self, base, arguments):
        self.id='new_object'
        self.expression1=base
        self.arguments=arguments
    def this_expression(self): 
        self.id='this'
    def super_expression(self): 
        self.id='super'
    def class_reference_expression(self):
        self.id='class_reference'
        
    def __str__(self, var_array_ref):
        if(self.id=='constant'):
            print("Constant(",self.expression1+'('+str(self.expression2)+')',")",end='')
        elif(self.id=='var'):
            name=''
            for i, v in enumerate(self.variable_table):
                if i == len(self.variable_table) - 1:
                    name+=(v.variable_name+')')
                else:
                    name+=(v.variable_name+',')
            print("Var(("+name+","+self.variable_table[0].type.type+")",end='')
        elif(self.id=='unary'):
            print("Unary(",self.operator1,', ',end='')
            self.expression1.__str__(var_array_ref)
            print(" )",end='')
        elif(self.id=='binary'):
            print("Binary(",self.operator1,', ',end='')
            self.expression1.__str__(var_array_ref)
            print(' , ',end='')
            self.expression2.__str__(var_array_ref)
            print(" )",end='')
        elif(self.id=='assign'):
            print("Assign( ",end='')
            self.expression1.__str__(var_array_ref)
            print(' , ',end='')
            self.expression2.__str__(var_array_ref)
            print(" )",end='')
        elif(self.id=='auto'):
            print("Auto( ",end='')
            self.expression1.__str__(var_array_ref)
            print(' ,',self.operator1,',',self.operator2,")",end='')
        elif(self.id=='field_access'):
            if(type(self.expression1) is str):
                print(self.expression1)
            if(type(self.expression2) is str):
                print(self.expression2)
            if(self.expression1==None):
                error=0
                for var_array in reversed(var_array_ref):
                    if self.expression2 in var_array:
                        error=1
                        if(var_array[self.expression2].variable_id>0):
                            print("Variable("+str(var_array[self.expression2].variable_id)+")",end='')
                        else:
                            print("Variable("+self.expression2+")",end='')
                        break
                if error==0:
                    print()
                    print("Variables Error: variables not uninitialized.")
                    print("Variable Name: "+self.expression2)
                    print()
                    sys.exit()
            else:
                if type(self.expression1) is str:
                    print("Field_access(",self.expression1,',',self.expression2,")",end='')
                else:
                    print("Field_access( ",end='')
                    self.expression1.__str__(var_array_ref)
                    print(' ,',self.expression2,")",end='')
        elif(self.id=='method_call'):
            if(self.expression1==None):
                print("Method_call( ",self.expression1,',',self.expression2,', [',end='')
            else:
                error=0
                if(self.expression1=='this' or self.expression1=='super'):
                    error=1
                    print("Method_call( ",self.expression1,',',self.expression2,', [',end='')
                else:
                    for var_array in reversed(var_array_ref):
                        if self.expression1 in var_array:
                            error=1
                            if(var_array[self.expression1].variable_id>0):
                                print("Method_call( Variable("+str(var_array[self.expression1].variable_id)+' ,',self.expression2,', [',end='')
                            else:
                                print("Method_call( ",self.expression1,',',self.expression2,', [',end='')
                            break
                if error==0:
                    print()
                    print("Variables Error: variables not uninitialized.")
                    print("Variable Name: '%s'" %(self.expression1))
                    print()
                    sys.exit()
            if(type(self.arguments) is list):
                for i, a in enumerate(self.arguments):
                    if i == len(self.arguments) - 1:
                        a.__str__(var_array_ref)
                    else:
                        a.__str__(var_array_ref)
                        print(' , ',end='')
            elif(self.arguments != None):
                    self.arguments.__str__(var_array_ref)
            print("] )",end='')
        elif(self.id=='new_object'):
            print("New_object(",self.expression1,', [',end='')
            if(type(self.arguments) is list):
                for i, a in enumerate(self.arguments):
                    if i == len(self.arguments) - 1:
                        a.__str__(var_array_ref)
                    else:
                        a.__str__(var_array_ref)
                        print(' , ',end='')
            elif(self.arguments != None):
                self.arguments.__str__(var_array_ref)
            print("] )",end='')
        elif(self.id=='this'):
            print("This",end='')
        elif(self.id=='super'):
            print("Super",end='')
        else:
            print("Class_reference",end='')
        return ''
    
def Initialization():
    type_int=Type('int')
    type_float=Type('float')
    type_boolean=Type('boolean')
    type_string=Type('string')
    
    scan_int=Method(['public', 'static'], type_int, 'scan_int', None, [])
    scan_float=Method(['public', 'static'], type_float, 'scan_float', None, [])
    Class('In', None, [scan_int, scan_float])
    
    vari=Variable('i')
    vari.type=type_int
    printi=Method(['public', 'static'], 'void', 'print', [vari], [])
    
    varf=Variable('f')
    varf.type=type_float
    printf=Method(['public', 'static'], 'void', 'print', [varf], [])
    
    varb=Variable('b')
    varb.type=type_boolean
    printb=Method(['public', 'static'], 'void', 'print', [varb], [])
    
    vars=Variable('s')
    vars.type=type_string
    prints=Method(['public', 'static'], 'void', 'print', [vars], [])
    Class('Out', None, [printi, printf, printb, prints])