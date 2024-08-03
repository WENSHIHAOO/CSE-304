#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521
from decaf_ast import *
from decaf_absmc import *

AM=Abstract_Machine()
class_static_field ={} #save offset
class_non_static_field ={} #save offset
argument_registers=0 #like a#
temporary_registers=0 # like t#
label_num=0 #like L#
Continue=''
Break=''
var_ref=[]
this=None
hload=True

def codegen_super(object):
    #find super
    if(class_table[object.class_name].super_class_name == None):
        return None
    return class_table[class_table[object.class_name].super_class_name]

def codegen_program():
    # set static_field
    global AM
    global class_static_field
    static_field_offset=0
    for Class in class_table.values():
        class_static_field[Class.class_name]={}
        for field in Class.fields:
            if(field.field_applicability == 'static'):
                class_static_field[Class.class_name][field.field_id]=static_field_offset
                static_field_offset+=1
    AM.print_static_data(static_field_offset)
    #set class
    for Class in class_table.values():
        AM.print_comments('\n#Class %s\n' %(Class.class_name))
        codegen_class(Class)
    return AM.machine_instructions

def codegen_class(object):
    # set non_static_field
    global AM
    global temporary_registers
    global class_non_static_field
    global this
    this = object
    class_non_static_field[object.class_name]={}
    super_class=codegen_super(object)
    non_static_field_offset=0
    if(super_class != None):
        class_non_static_field[object.class_name].update(class_non_static_field[super_class.class_name])
        non_static_field_offset=len(class_non_static_field[super_class.class_name])
    for field in object.fields:
        if(field.field_applicability == 'non-static'):
            class_non_static_field[object.class_name][field.field_id]=non_static_field_offset
            non_static_field_offset+=1
    
    if(non_static_field_offset>0):
        AM.print_comments('\t#Non-static Fileds is %d\n\n' %(non_static_field_offset))
        
    #set constructor
    for constructor in object.class_constructors:
        AM.print_label('C_%d' %(constructor.constructor_id))
        codegen_constructor(constructor)
    #set method
    for method in object.methods.values():
        AM.print_label('M_%s_%d' %(method.method_name, method.method_id))
        codegen_method(method)
    return None

def codegen_constructor(object):
    global AM
    global argument_registers
    global temporary_registers
    global var_ref
    var_ref.append(object.constructor_parameters)
    var_ref.append(object.variable_table)
    if(len(object.constructor_parameters) != 0):
        for p in object.constructor_parameters.values():
            p.register='a'+str(argument_registers)
            argument_registers+=1
            AM.print_comments('\t#formal %s for %s\n' %(p.variable_name, p.register))
        AM.print_comments('\n')
        
    for stmt in object.constructor_body:
        #
        if(type(stmt) is Expression and stmt.id == 'var'):
            codegen_index(stmt)
        else:
            save_temporary_registers=temporary_registers
            codegen_index(stmt)
            temporary_registers=save_temporary_registers
        AM.print_comments('\n')
        #
    var_ref.pop()
    var_ref.pop()
    argument_registers=0
    temporary_registers=0
    AM.ret()
    AM.print_comments('\n')
    return None

def codegen_method(object):
    global AM
    global argument_registers
    global temporary_registers
    global var_ref
    var_ref.append(object.method_parameters)
    var_ref.append(object.variable_table)
    if(object.method_applicability == 'non-static'):
        argument_registers+=1
        AM.print_comments('\t#this for a0\n')
        AM.print_comments('\n')
    if(len(object.method_parameters) != 0):
        for p in object.method_parameters.values():
            p.register='a'+str(argument_registers)
            argument_registers+=1
            AM.print_comments('\t#formal %s for %s\n' %(p.variable_name, p.register))
        AM.print_comments('\n')
    
    for stmt in object.method_body:
        #
        if(type(stmt) is Expression and stmt.id == 'var'):
            codegen_index(stmt)
        else:
            save_temporary_registers=temporary_registers
            codegen_index(stmt)
            temporary_registers=save_temporary_registers
        AM.print_comments('\n')
        #
    var_ref.pop()
    var_ref.pop()
    argument_registers=0
    temporary_registers=0
    return None

def codegen_index(object):
    global AM
    global temporary_registers
    if(object == None):
        return None
    elif(type(object) is str):
        return None
    elif(type(object) is list):
        for i in list:
            #
            if(type(i) is Expression and i.id == 'var'):
                codegen_index(i)
            else:
                save_temporary_registers=temporary_registers
                codegen_index(i)
                temporary_registers=save_temporary_registers
                #
    elif(type(object) is Variable):
        return None
    elif(type(object) is Type):
        return None
    
    elif(type(object) is Statement):
        if(object.id=='if'):
            codegen_Statement.codegen_if_stmt(object)
        elif(object.id=='while'):
            codegen_Statement.codegen_while_stmt(object)
        elif(object.id=='for'):
            codegen_Statement.codegen_for_stmt(object)
        elif(object.id=='return'):
            codegen_Statement.codegen_return_stmt(object)
        elif(object.id=='expr'):
            codegen_Statement.codegen_expr_stmt(object)
        elif(object.id=='block'):
            codegen_Statement.codegen_block_stmt(object)
        elif(object.id=='break'):
            global Break
            AM.jmp(Break)
        elif(object.id=='continue'):
            global Continue
            AM.jmp(Continue)
        elif(object.id=='skip'):
            return None
        
    elif(type(object) is Expression):
        if(object.id=='constant'):
            return codegen_Expression.codegen_constant_expression(object)
        elif(object.id=='var'):
            return codegen_Expression.codegen_var_expression(object)
        elif(object.id=='unary'):
            return codegen_Expression.codegen_unary_expression(object)
        elif(object.id=='binary'):
            return codegen_Expression.codegen_binary_expression(object)
        elif(object.id=='assign'):
            return codegen_Expression.codegen_assign_expression(object)
        elif(object.id=='auto'):
            return codegen_Expression.codegen_auto_expression(object, None)
        elif(object.id=='field_access'):
            return codegen_Expression.codegen_field_access_expression(object)
        elif(object.id=='method_call'):
            return codegen_Expression.codegen_method_call_expression(object)
        elif(object.id=='new_object'):
            return codegen_Expression.codegen_new_object_expression(object)
        elif(object.id=='this'):
            return codegen_Expression.codegen_this_expression(object)
        elif(object.id=='super'):
            return codegen_Expression.codegen_super_expression(object)
        elif(object.id=='class_reference'):
            return codegen_Expression.codegen_class_reference_expression(object)
    return None

class codegen_Statement(object):
    def codegen_if_stmt(stmt):
        global AM
        global label_num
        global temporary_registers
        global var_ref
        #condition
        codegen_index(stmt.condition)
        label1='L'+str(label_num)
        label_num+=1
        AM.bz(stmt.condition.register, label1)
        #then
        if(type(stmt.then_stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.then_stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    codegen_index(s)
                else:
                    save_temporary_registers=temporary_registers
                    codegen_index(s)
                    temporary_registers=save_temporary_registers
                AM.print_comments('\n')
                #
            var_ref.pop()
        else:
            codegen_index(stmt.then_stmt)
        label2=''
        if(stmt.stmt != None):
            label2='L'+str(label_num)
            label_num+=1
            AM.jmp(label2)
        #else
        AM.print_label(label1)
        if(stmt.stmt != None):
            if(type(stmt.stmt) is list):
                var_ref.append(stmt.check_var)
                for s in stmt.stmt:
                    #
                    if(type(s) is Expression and s.id == 'var'):
                        codegen_index(s)
                    else:
                        save_temporary_registers=temporary_registers
                        codegen_index(s)
                        temporary_registers=save_temporary_registers
                    AM.print_comments('\n')
                    #
                var_ref.pop()
            else:
                codegen_index(stmt.stmt)   
            AM.print_label(label2)
        return None

    def codegen_while_stmt(stmt):
        global AM
        global label_num
        global temporary_registers
        global var_ref
        #condition
        label1='L'+str(label_num)
        label_num+=1
        global Continue
        Continue=label1
        AM.print_comments('#%s for Continue\n' %(Continue))
        AM.print_label(label1)
        codegen_index(stmt.condition)
        label2='L'+str(label_num)
        label_num+=1
        global Break
        Break=label2
        AM.bz(stmt.condition.register, label2)
        #stmt
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    codegen_index(s)
                else:
                    save_temporary_registers=temporary_registers
                    codegen_index(s)
                    temporary_registers=save_temporary_registers
                AM.print_comments('\n')
                #
            var_ref.pop()
        else:
            codegen_index(stmt.stmt)
        AM.jmp(label1)
        AM.print_comments('#%s for Break\n' %(Break))
        AM.print_label(label2)
        return None

    def codegen_for_stmt(stmt):
        global AM
        global label_num
        global temporary_registers
        global var_ref
        #initializer
        codegen_index(stmt.initializer)
        #condition
        label1='L'+str(label_num)
        label_num+=1
        AM.print_label(label1)
        codegen_index(stmt.condition)
        label2='L'+str(label_num)
        label_num+=1
        global Break
        Break=label2
        AM.bz(stmt.condition.register, label2)
        #stmt
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    codegen_index(s)
                else:
                    save_temporary_registers=temporary_registers
                    codegen_index(s)
                    temporary_registers=save_temporary_registers
                AM.print_comments('\n')
                #
            var_ref.pop()
        else:
            codegen_index(stmt.stmt)
        #update
        label3='L'+str(label_num)
        label_num+=1
        global Continue
        Continue=label3
        AM.print_comments('#%s for Continue\n' %(Continue))
        AM.print_label(label3)
        codegen_index(stmt.update)
        AM.jmp(label1)
        AM.print_comments('#%s for Break\n' %(Break))
        AM.print_label(label2)
        return None

    def codegen_return_stmt(stmt):
        global AM
        if(stmt.expr != None):
            codegen_index(stmt.expr)
            AM.move('a0', stmt.expr.register)
        AM.ret()
        return None

    def codegen_expr_stmt(stmt):
        global temporary_registers
        global var_ref
        if(type(stmt.expr) is list):
            var_ref.append(stmt.check_var)
            for e in stmt.expr:
                #
                if(type(e) is Expression and e.id == 'var'):
                    codegen_index(e)
                else:
                    save_temporary_registers=temporary_registers
                    codegen_index(e)
                    temporary_registers=save_temporary_registers
                AM.print_comments('\n')
                #
            var_ref.pop()
        else:
            codegen_index(stmt.expr)
        return None

    def codegen_block_stmt(stmt):
        global temporary_registers
        global var_ref
        if(type(stmt.stmt) is list):
            var_ref.append(stmt.check_var)
            for s in stmt.stmt:
                #
                if(type(s) is Expression and s.id == 'var'):
                    codegen_index(s)
                else:
                    save_temporary_registers=temporary_registers
                    codegen_index(s)
                    temporary_registers=save_temporary_registers
                AM.print_comments('\n')
                #
            var_ref.pop()
        else:
            codegen_index(stmt.stmt)
        return None

class codegen_Expression():
    def codegen_constant_expression(expr):
        #assume no string, no null
        global AM
        global temporary_registers
        if(expr.expression1 == 'int'):
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move_immed_i(expr.register, expr.expression2)
        elif(expr.expression1 == 'float'):
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move_immed_f(expr.register, expr.expression2)
        elif(expr.expression1 == 'boolean'):
            if(expr.expression2=='true'):
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.move_immed_i(expr.register, 1)
            elif(expr.expression2=='false'):
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.move_immed_i(expr.register, 0)
        return None

    def codegen_var_expression(expr):
        global AM
        global temporary_registers
        for var in expr.variable_table:
            var.register='t'+str(temporary_registers)
            temporary_registers+=1
            AM.print_comments('\t#local %s for %s\n' %(var.variable_name, var.register))
        return None

    def codegen_unary_expression(expr):
        global AM
        global temporary_registers
        codegen_index(expr.expression1)
        #+
        if(expr.operator1=='+'):
            expr.register=expr.expression1.register
            return None
        #!, -
        expr.register='t'+str(temporary_registers)
        temporary_registers+=1
        if(expr.operator1=='!'):
            AM.move_immed_i(expr.register, 1)
            AM.isub(expr.register, expr.register, expr.expression1.register)
        elif(expr.operator1=='-'):
            if(expr.expression1.typecheck == 'int'):
                AM.move_immed_i(expr.register, -1)
                AM.imul(expr.register, expr.register, expr.expression1.register)
            elif(expr.expression1.typecheck == 'float'):
                AM.move_immed_f(expr.register, -1.0)
                AM.fmul(expr.register, expr.register, expr.expression1.register) 
        return None

    def codegen_binary_expression(expr):
        global AM
        global label_num
        global temporary_registers
        codegen_index(expr.expression1)
        
        #'add', 'sub', 'mul', 'div'
        if(expr.operator1=='add'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fadd(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fadd(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fadd(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.iadd(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1=='sub'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fsub(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fsub(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fsub(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.isub(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1=='mul'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fmul(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fmul(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fmul(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.imul(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1=='div'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fdiv(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fdiv(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fdiv(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.idiv(expr.register, expr.expression1.register, expr.expression2.register)
        
        #'and', 'or'
        elif(expr.operator1 == 'and'):
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move(expr.register, expr.expression1.register)
            label1='L'+str(label_num)
            label_num+=1
            AM.bz(expr.register, label1)
            codegen_index(expr.expression2)
            AM.move(expr.register, expr.expression2.register)
            AM.print_label(label1)
        elif(expr.operator1 == 'or'):
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move(expr.register, expr.expression1.register)
            label1='L'+str(label_num)
            label_num+=1
            AM.bnz(expr.register, label1)
            codegen_index(expr.expression2)
            AM.move(expr.register, expr.expression2.register)
            AM.print_label(label1)
            
        #'lt', 'leq', 'gt', 'geq'
        elif(expr.operator1 == 'lt'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.flt(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.flt(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.flt(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.ilt(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1 == 'leq'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fleq(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fleq(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fleq(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.ileq(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1 == 'gt'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fgt(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fgt(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fgt(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.igt(expr.register, expr.expression1.register, expr.expression2.register)
        elif(expr.operator1 == 'geq'):
            codegen_index(expr.expression2)
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    AM.itof(expr.register, expr.expression2.register)
                    AM.fgeq(expr.register, expr.expression1.register, expr.register)
                #1='float', 2='float'
                else:
                    AM.fgeq(expr.register, expr.expression1.register, expr.expression2.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                AM.itof(expr.register, expr.expression1.register)
                AM.fgeq(expr.register, expr.register, expr.expression2.register)
            else:
                #1='int', 2='int'
                AM.igeq(expr.register, expr.expression1.register, expr.expression2.register)
        
        #'eq', 'neq'
        elif(expr.operator1 == 'eq'):
            codegen_index(expr.expression2)
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    expr.register='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.itof(expr.register, expr.expression2.register)
                    r1='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fgeq(r1, expr.expression1.register, expr.register)
                    r2='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fleq(r2, expr.expression1.register, expr.register)
                    AM.imul(expr.register, r1, r2)
                #1='float', 2='float'
                else:
                    r1='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fgeq(r1, expr.expression1.register, expr.expression2.register)
                    r2='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fleq(r2, expr.expression1.register, expr.expression2.register)
                    expr.register='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.imul(expr.register, r1, r2)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.itof(expr.register, expr.expression1.register)
                r1='t'+str(temporary_registers)
                temporary_registers+=1
                AM.fgeq(r1, expr.register, expr.expression2.register)
                r2='t'+str(temporary_registers)
                temporary_registers+=1
                AM.fleq(r2, expr.register, expr.expression2.register)
                AM.imul(expr.register, r1, r2)
            else:
                #1='int', 2='int'
                r1='t'+str(temporary_registers)
                temporary_registers+=1
                AM.igeq(r1, expr.expression1.register, expr.expression2.register)
                r2='t'+str(temporary_registers)
                temporary_registers+=1
                AM.ileq(r2, expr.expression1.register, expr.expression2.register)
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.imul(expr.register, r1, r2)
        elif(expr.operator1 == 'neq'):
            codegen_index(expr.expression2)
            if(expr.expression1.typecheck=='float'):
                #1='float', 2='int'
                if(expr.expression2.typecheck=='int'):
                    expr.register='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.itof(expr.register, expr.expression2.register)
                    r1='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fgeq(r1, expr.expression1.register, expr.register)
                    r2='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fleq(r2, expr.expression1.register, expr.register)
                    AM.imul(expr.register, r1, r2)
                    AM.move_immed_i(r1, 1)
                    AM.isub(expr.register, r1, expr.register)
                #1='float', 2='float'
                else:
                    r1='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fgeq(r1, expr.expression1.register, expr.expression2.register)
                    r2='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.fleq(r2, expr.expression1.register, expr.expression2.register)
                    expr.register='t'+str(temporary_registers)
                    temporary_registers+=1
                    AM.imul(expr.register, r1, r2)
                    AM.move_immed_i(r1, 1)
                    AM.isub(expr.register, r1, expr.register)
            elif(expr.expression2.typecheck=='float'):
                #1='int', 2='float'
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.itof(expr.register, expr.expression1.register)
                r1='t'+str(temporary_registers)
                temporary_registers+=1
                AM.fgeq(r1, expr.register, expr.expression2.register)
                r2='t'+str(temporary_registers)
                temporary_registers+=1
                AM.fleq(r2, expr.register, expr.expression2.register)
                AM.imul(expr.register, r1, r2)
                AM.move_immed_i(r1, 1)
                AM.isub(expr.register, r1, expr.register)
            else:
                #1='int', 2='int'
                r1='t'+str(temporary_registers)
                temporary_registers+=1
                AM.igeq(r1, expr.expression1.register, expr.expression2.register)
                r2='t'+str(temporary_registers)
                temporary_registers+=1
                AM.ileq(r2, expr.expression1.register, expr.expression2.register)
                expr.register='t'+str(temporary_registers)
                temporary_registers+=1
                AM.imul(expr.register, r1, r2)
                AM.move_immed_i(r1, 1)
                AM.isub(expr.register, r1, expr.register)
        return None

    def codegen_assign_expression(expr):
        global hload
        global AM
        if(type(expr.expression1) is Expression and expr.expression1.id=='field_access'):
            hload=False
        codegen_index(expr.expression1)
        hload=True
        if(type(expr.expression2) is Expression and expr.expression2.operator2=='post'):
            codegen_Expression.codegen_auto_expression(expr.expression2, expr.expression1)
        else:
            codegen_index(expr.expression2)
        if(not (type(expr.expression2) is Expression and expr.expression2.operator2=='post')):
            AM.move(expr.expression1.register, expr.expression2.register)
        expr.register=expr.expression1.register
        
        if(type(expr.expression1) is Expression and expr.expression1.base_register!=None):
            AM.hstore(expr.expression1.base_register, expr.expression1.offset_register, expr.expression1.register)
        return None

    def codegen_auto_expression(expr, assign):
        global AM
        global temporary_registers
        codegen_index(expr.expression1)
        if(assign != None and expr.operator2=='post'):
            AM.move(assign.register, expr.expression1.register)
        expr.register=expr.expression1.register
        r1='t'+str(temporary_registers)
        temporary_registers+=1
        if(expr.operator1 == 'auto-increment'):
            if(expr.expression1.typecheck=='int'):
                AM.move_immed_i(r1, 1)
                AM.iadd(expr.register, expr.register, r1)
            else:
                AM.move_immed_f(r1, 1.0)
                AM.fadd(expr.register, expr.register, r1)
        else:
            if(expr.expression1.typecheck=='int'):
                AM.move_immed_i(r1, 1)
                AM.isub(expr.register, expr.register, r1)
            else:
                AM.move_immed_f(r1, 1.0)
                AM.fsub(expr.register, expr.register, r1)
        if(type(expr.expression1) is Expression and expr.expression1.base_register!=None):
            AM.hstore(expr.expression1.base_register, expr.expression1.offset_register, expr.expression1.register)
        return None

    def codegen_field_access_expression(expr):
        global this
        global AM
        global var_ref
        #lhs
        if(expr.expression1==None):
            for array in reversed(var_ref):
                if expr.expression2 in array:
                    expr.register=array[expr.expression2].register
                    return None
            codegen_name_resolution(this, expr)
            return None
        #p.x: z
        else:
            if(expr.expression1.expression1==None):
                expression1=expr.expression1.expression2
                for array in reversed(var_ref):
                    if expression1 in array:
                        #'user'
                        codegen_name_resolution(class_table[array[expression1].type.type], expr)
                        return None
                if(expression1 == 'this'):
                    #'user'
                    codegen_name_resolution(this, expr)
                    return None
                elif(expression1 == 'super'):
                    s=codegen_super(this)
                    #'user'
                    codegen_name_resolution(s, expr)
                    return None
                elif expression1 in class_table:
                    #'classliteral'
                    codegen_name_resolution(class_table[expression1], expr)
                    return None
            else:
                codegen_index(expr.expression1)
                #'user'
                codegen_name_resolution(class_table[expr.expression1.typecheck], expr)
                return None
        return None

    def codegen_method_call_expression(expr):
        #f(e_1, ..., e_n): h
        if(expr.expression1.expression1==None):
            codegen_name_resolution(None, expr)
        ##p.f(e_1, ..., e_n): h
        else:
            expression1=expr.expression1
            if(expression1.expression1.expression1==None):
                #'user'
                codegen_name_resolution(None, expr)
            else:
                #'user'
                codegen_index(expression1.expression1)
                codegen_name_resolution(None, expr)
        return None

    def codegen_new_object_expression(expr):
        global AM
        global temporary_registers
        global class_non_static_field
        global argument_registers
        #new A(e_1, ..., e_n)
        if(expr.arguments != None):
            for e in expr.arguments:
                codegen_index(e)
        #halloc
        r1='t'+str(temporary_registers)
        temporary_registers+=1
        AM.move_immed_i(r1, len(class_non_static_field[expr.expression1]))
        expr.register='t'+str(temporary_registers)
        temporary_registers+=1
        AM.halloc(expr.register, r1)
        #save
        for i in range(0, argument_registers):
            AM.save('a'+str(i))
        for i in range(0, temporary_registers):
            AM.save('t'+str(i))  
        #move
        AM.move('a0', expr.register)
        if(expr.arguments != None):
            j=1
            for e in expr.arguments:
                AM.move('a'+str(j), e.register)
                j+=1
        #call
        AM.call("C_%d" % (expr.constructor_id))
        #restore
        for i in range(temporary_registers-1, -1, -1):
            AM.restore('t'+str(i)) 
        for i in range(argument_registers-1, -1, -1):
            AM.restore('a'+str(i))
        return None

    def codegen_this_expression(expr):
        expr.register='a0'
        return None

    def codegen_super_expression(expr):
        return None

    def codegen_class_reference_expression(expr):
        return None

def codegen_name_resolution(p, expr):
    global AM
    global temporary_registers
    global argument_registers
    global class_non_static_field
    global class_static_field
    global hload
    if(expr.id=='field_access'):
        if(expr.field_id in class_non_static_field[p.class_name]):
            r1='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move_immed_i(r1, id(class_non_static_field[p.class_name]))# base address
            r2='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move_immed_i(r2, class_non_static_field[p.class_name][expr.field_id])# offset
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(hload):
                AM.hload(expr.register, r1, r2)
            expr.base_register=r1
            expr.offset_register=r2
        else:
            r2='t'+str(temporary_registers)
            temporary_registers+=1
            AM.move_immed_i(r2, class_static_field[p.class_name][expr.field_id])# offset
            expr.register='t'+str(temporary_registers)
            temporary_registers+=1
            if(hload):
                AM.hload(expr.register, 'sap', r2)
            expr.base_register='sap'
            expr.offset_register=r2
    elif(expr.id=='method_call'):  
        if(expr.arguments != None):
            for e in expr.arguments:
                codegen_index(e)
        #save
        for i in range(0, argument_registers):
            AM.save('a'+str(i))
        for i in range(0, temporary_registers):
            AM.save('t'+str(i))  
        #move
        if(expr.arguments != None):
            j=0
            for e in expr.arguments:
                AM.move('a'+str(j), e.register)
                j+=1
        #call
        AM.call("M_%s_%d" % (expr.expression1.expression2 , expr.method_id))
        expr.register='t'+str(temporary_registers)
        temporary_registers+=1
        AM.move(expr.register, 'a0')
        #restore
        for i in range(temporary_registers-2, -1, -1):
            AM.restore('t'+str(i)) 
        for i in range(argument_registers-1, -1, -1):
            AM.restore('a'+str(i))
    return None