from Constants import *

class VMWriter:
    def __init__(self):
        self.subroutine_type_declared = ""
        self.return_type = ""
        self.nFields = 0
        
    def setNFields(self, nFields):
        self.nFields = nFields
        
    def setSubroutineTypeDeclared(self, subroutine_type_declared):
        self.subroutine_type_declared = subroutine_type_declared

    def setReturnType(self, return_type):
        self.return_type = return_type

    def writePush(self, segment, index):
        if segment == "constant":
            vm_line = f"push constant {index}"
            return vm_line
        elif segment in WRITE_MEMORY_MAP:
            vm_line = f"push {WRITE_MEMORY_MAP[segment]} {index}"
            return vm_line
    
    def writePop(self,segment, index):
        if segment in WRITE_MEMORY_MAP:
            vm_line = f"pop {WRITE_MEMORY_MAP[segment]} {index}"
            return vm_line

    def writeArithmetic(self, command):
        if command in WRITE_ARITHMETIC_MAP:
            return WRITE_ARITHMETIC_MAP[command]
        elif command == "MULTIPLY":
            vm_line = "call Math.multiply 2"
            return vm_line
        elif command == "DIVIDE":
            vm_line = "call Math.divide 2"
            return vm_line
            
    def writeLabel(self, label):
        vm_line = f"label {label}"
        return vm_line
    
    def writeGoto(self, label):
        vm_line = f"goto {label}"
        return vm_line
    
    def writeIf(self, label):
        vm_line = f"if-goto {label}"
        return vm_line
    
    def writeCall(self, function_name, nArgs):

        vm_line = f"call {function_name} {nArgs}"
        return vm_line
    
    def writeFunction(self, function_name, nVars):

        vm_line = []
        
        vm_line.append(f"function {function_name} {nVars}")
        
        if self.subroutine_type_declared == "method":
            vm_line.append(self.writePush("arg", 0))
            vm_line.append(self.writePop("pointer", 0))

        if self.subroutine_type_declared == "constructor":
            vm_line.append(self.writePush("constant", self.nFields))
            vm_line.append(self.writeCall("Memory.alloc", 1))
            vm_line.append(self.writePop("pointer", 0))


           
        
        return vm_line
    
    def writeReturn(self):
        vm_line = "return"
        return vm_line
    
    # def close(self):
    
    
# codeWrite(exp):
# if exp is a constant c 
    # output "push c"
# if exp is a variable var 
    # output "push var"
# if exp is "expl op exp2" 
    # codeWrite(exp1,) 
    # codeWrite(exp2) 
    # output"op"
# if exp is "op exp" 
    # codeWrite(exp) 
    # output "op"
# if exp is "f(exp1 ... expN)"
    # codeWrite(exp1)
    # ...
    # codeWrite(expN 
    # output "call f n"