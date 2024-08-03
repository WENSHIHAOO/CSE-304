#Name: Shihao Wen
#Netid: shiwen
#Student ID: 113085521

import sys
code=[]
label={}
store={}
stack=[]

def clean_input(input):
    index=0
    str=""
    charASCII=0
    while(index<len(input)):#Save the number, label and instruction separately into code[] or label[]
        charASCII=ord(input[index])
        if(charASCII==32 or charASCII==9 or charASCII==10 or charASCII==35):#blank, tab, newline, and comment
            if(charASCII==35):#clean comment
                while(index<len(input) and charASCII!=10):
                    index+=1
                    charASCII=ord(input[index])
            if(str!=""):#Put the number or instruction into the code[]
                code.append(str)
                str=""
        elif(64<charASCII<91 or 96<charASCII<123 or charASCII==95):#letter or '_'
            if(charASCII==95 and str==""):#The first character of str is '_'
                print("Error: \'_\' position error")
                sys.exit()
            else:
                str+=input[index]
        elif(charASCII==45):# '-'
            if(str=="" and 47<ord(input[index+1])<58):#'-' can only appear in the first place, and there must be numbers after it
                str+=input[index]
            else:
                print("Error: \'-\' position error")
                sys.exit()
        elif(47<ord(input[index])<58):#number
            str+=input[index]
        elif(charASCII==58):# ':'
            if(str == "" or ord(str[0])==45 or 47<ord(str[0])<58):#str is empty or "-" or a number
                print("Error: \':\' position error")
                sys.exit()
            else:#Put the label into label[]
                label[str]=len(code)
                str=""
        index+=1
    if(str!=""):#Put the number or instruction into code[]
        code.append(str)
        str=""
        
def check_label_format():
    lastDic=-1
    for i in label:
        if(label[i]==len(code)):#code[] the last one is label
            print("Error: Nothing after in label")
            sys.exit()
        if(label[i]!=lastDic):#Different labels have different values
            lastDic=label[i]
        else:
            print("Error: multiple label")
            sys.exit()
        
def check_instr_format():
    index=0
    label_instr=("jz", "jnz", "jmp")
    instructions=("ildc", "iadd", "isub", "imul", "idiv", "imod", "pop", 
              "dup", "swap", "jz", "jnz", "jmp", "load", "store")
    while(index<len(code)):
        if(code[index] in label_instr):
            if(code[index+1] not in label):#There is no label behind the label instruction
                print("Error: No such label")
                sys.exit()
        elif(code[index] == "ildc"):
            if(not((47<ord(code[index+1][0])<58) or (ord(code[index+1][0])==45))):#no number after ildc
                print("Error: No int after ildc")
                sys.exit()
        elif(ord(code[index][0])==45 or 47<ord(code[index][0])<58):
            index+=1
            continue
        elif((code[index] not in instructions) and (code[index] not in label) and (code[index][:len(code[index])-1] not in label)):
            print("Error: No such instructions")
            sys.exit()
        index+=1
    
def pop():
    try:
        return stack.pop()
    except IndexError:
        print("Error: Index error")
        sys.exit()

def jump(lab):
    execution(label[lab])
    if(len(stack)==1):#When the stack has only one number, get the answer
        return True
    return False

def execution(i):
    pop1=0
    pop2=0
    while(i<len(code)):
        if(code[i]=="ildc"):
            i+=1
            stack.append(code[i])
        elif(code[i]=="iadd"):
            pop1=pop()
            pop2=pop()
            stack.append(int(pop2)+int(pop1))
        elif(code[i]=="isub"):
            pop1=pop()
            pop2=pop()
            stack.append(int(pop2)-int(pop1))
        elif(code[i]=="imul"):
            pop1=pop()
            pop2=pop()
            stack.append(int(pop2)*int(pop1))
        elif(code[i]=="idiv"):
            pop1=pop()
            pop2=pop()
            stack.append(int(pop2)/int(pop1))
        elif(code[i]=="imod"):
            pop1=pop()
            pop2=pop()
            stack.append(int(pop2)%int(pop1))
        elif(code[i]=="pop"):
            pop()
        elif(code[i]=="dup"):
            stack.append(stack[-1])
        elif(code[i]=="swap"):
            pop1=pop()
            pop2=pop()
            stack.append(pop1)
            stack.append(pop2)
        elif(code[i]=="jz"):
            i+=1
            pop1=pop()
            if(pop1==0):
                if(jump(code[i])):
                    break
        elif(code[i]=="jnz"):
            i+=1
            pop1=pop()
            if(pop1!=0):
                if(jump(code[i])):
                    break
        elif(code[i]=="jmp"):
            i+=1
            if(jump(code[i])):
                    break
        elif(code[i]=="load"):
            index=pop()
            try:
                stack.append(store[index])
            except KeyError:
                print("Error: Noting in the index")
                sys.exit()
        elif(code[i]=="store"):
            pop1=pop()
            index=pop()
            store[index]=pop1
        i+=1
    if(len(stack)==0):
        return "Nothing"
    else:
        return stack[0]

if(len(sys.argv)>1):
    input = open(sys.argv[1]).read()
else:
    if(sys.stdin.isatty()):
        print("Error: No input")
        sys.exit()
    else:
        input = sys.stdin.read()

clean_input(input)
check_label_format()
check_instr_format()
print(execution(0))