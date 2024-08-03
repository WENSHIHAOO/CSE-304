#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521

class Abstract_Machine:
    def __init__(self):
        self.machine_instructions=''
    
    def print_static_data(self, i):
        self.machine_instructions+=('.static_data %d\n' %(i))
        
    def print_label(self, L):
        self.machine_instructions+=('%s:\n' %(L))
        
    def print_comments(self, C):
        self.machine_instructions+=C
    #Move:
    def move_immed_i(self, r, i):
        self.machine_instructions+=('\tmove_immed_i %s, %d\n' %(r, i))
        
    def move_immed_f(self, r, f):
        self.machine_instructions+=('\tmove_immed_f %s, %f\n' %(r, f))

    def move (self, r1, r2) :
        self.machine_instructions+=('\tmove %s, %s\n' %(r1, r2))
        
        
    #Integer Arithmetic:
    def iadd(self, r1, r2, r3):
        self.machine_instructions+=('\tiadd %s, %s, %s\n' %(r1, r2, r3))
        
    def isub(self, r1, r2, r3):
        self.machine_instructions+=('\tisub %s, %s, %s\n' %(r1, r2, r3))
        
    def imul(self, r1, r2, r3):
        self.machine_instructions+=('\timul %s, %s, %s\n' %(r1, r2, r3))
        
    def idiv(self, r1, r2, r3):
        self.machine_instructions+=('\tidiv %s, %s, %s\n' %(r1, r2, r3))
        
    def imod(self, r1, r2, r3):
        self.machine_instructions+=('\timod %s, %s, %s\n' %(r1, r2, r3))
        
    def igt(self, r1, r2, r3):
        self.machine_instructions+=('\tigt %s, %s, %s\n' %(r1, r2, r3))
        
    def igeq(self, r1, r2, r3):
        self.machine_instructions+=('\tigeq %s, %s, %s\n' %(r1, r2, r3))
        
    def ilt(self, r1, r2, r3):
        self.machine_instructions+=('\tilt %s, %s, %s\n' %(r1, r2, r3))
        
    def ileq(self, r1, r2, r3):
        self.machine_instructions+=('\tileq %s, %s, %s\n' %(r1, r2, r3))
        

    #Floating Point Arithmetic:
    def fadd(self, r1, r2, r3):
        self.machine_instructions+=('\tfadd %s, %s, %s\n' %(r1, r2, r3))
        
    def fsub(self, r1, r2, r3):
        self.machine_instructions+=('\tfsub %s, %s, %s\n' %(r1, r2, r3))
        
    def fmul(self, r1, r2, r3):
        self.machine_instructions+=('\tfmul %s, %s, %s\n' %(r1, r2, r3))
        
    def fdiv(self, r1, r2, r3):
        self.machine_instructions+=('\tfdiv %s, %s, %s\n' %(r1, r2, r3))
        
    def fgt(self, r1, r2, r3):
        self.machine_instructions+=('\tfgt %s, %s, %s\n' %(r1, r2, r3))
        
    def fgeq(self, r1, r2, r3):
        self.machine_instructions+=('\tfgeq %s, %s, %s\n' %(r1, r2, r3))
        
    def flt(self, r1, r2, r3):
        self.machine_instructions+=('\tflt %s, %s, %s\n' %(r1, r2, r3))
        
    def fleq(self, r1, r2, r3):
        self.machine_instructions+=('\tfleq %s, %s, %s\n' %(r1, r2, r3))
        
    
    #Conversions:
    def ftoi(self, r1, r2):
        self.machine_instructions+=('\tftoi %s, %s\n' %(r1, r2))
        
    def itof(self, r1, r2):
        self.machine_instructions+=('\titof %s, %s\n' %(r1, r2))
        

    #Branches:
    def bz(self, r1, L):
        self.machine_instructions+=('\tbz %s, %s\n' %(r1, L))
        
    def bnz(self, r1, L):
        self.machine_instructions+=('\tbnz %s, %s\n' %(r1, L))
        
    def jmp(self, L):
        self.machine_instructions+=('\tjmp %s\n' %(L))
        

    #Heap Manipulation:
    def hload(self, r1, r2, r3):
        self.machine_instructions+=('\thload %s, %s, %s\n' %(r1, r2, r3))
        
    def hstore(self, r1, r2, r3):
        self.machine_instructions+=('\thstore %s, %s, %s\n' %(r1, r2, r3))
        
    def halloc(self, r1, r2):
        self.machine_instructions+=('\thalloc %s, %s\n' %(r1, r2))
        

    #Procedure Call and Return:
    def call(self, L):
        self.machine_instructions+=('\tcall %s\n' %(L))
        
    def ret(self):
        self.machine_instructions+=('\tret\n')
        
    def save(self, r):
        self.machine_instructions+=('\tsave %s\n' %(r))
        
    def restore(self, r):
        self.machine_instructions+=('\trestore %s\n' %(r))