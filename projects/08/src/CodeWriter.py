SEGMENT_DICT = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "temp": "TEMP", "R13": "R13", "R14": "R14", "R15": "R15"}

class CodeWriter:
    def __init__(self):
        self.addrMap = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, 
                        "TEMP": 5, "R13": 13, "R14": 14, "R15": 15,
                        "static": 256}
        self.eqNumber = 0
        self.gtNumber = 0
        self.ltNumber = 0
        self.staticNumber = 16
        self.currentFile = ""
        self.retAddrCount = 0
        self.currentFunction = ""
        
    def setCurrentFunction(self, function): 
        self.currentFunction = function
        
        
    def setCurrentFile(self, file_name):
        self.currentFile = file_name
    
    def writeArithmetic(self, command):
        if command == "add":
            return ["// add", "@SP", "M=M-1", "@SP", "A=M", "D=M", "@SP", "A=M-1", "M=D+M"]
        elif command == "sub":
            return ["// sub", "@SP", "M=M-1", "@SP", "A=M", "D=M", "@SP", "A=M-1", "M=M-D"]
        elif command == "neg":
            return ["// neg", "@SP", "A=M-1", "M=-M"]
        elif command == "eq":
            label_1 = f"{self.currentFile}.eq.{self.eqNumber}"
            self.eqNumber =  self.eqNumber + 1
            label_2 = f"{self.currentFile}.eq.{self.eqNumber}" 
            asm_line = ["// eq", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "D=M-D", f"@{label_1}", "D;JEQ", "@SP", "A=M-1", "M=0", f"@{label_2}", "0;JMP", f"({label_1})", "@SP", "A=M-1", "M=-1", f"({label_2})"]
            self.eqNumber =  self.eqNumber + 1
            return asm_line
            
        elif command == "gt":
            label_1 = f"{self.currentFile}.gt.{self.gtNumber}"
            self.gtNumber =  self.gtNumber + 1
            label_2 = f"{self.currentFile}.gt.{self.gtNumber}"
            asm_line = ["// gt", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "D=M-D", f"@{label_1}", "D;JGT", "@SP", "A=M-1", "M=0", f"@{label_2}", "0;JMP", f"({label_1})", "@SP", "A=M-1", "M=-1", f"({label_2})"]
            self.gtNumber =  self.gtNumber + 1
            return asm_line
            
        elif command == "lt":
            label_1 = f"{self.currentFile}.lt.{self.ltNumber}"
            self.ltNumber =  self.ltNumber + 1
            label_2 = f"{self.currentFile}.lt.{self.ltNumber}"
            asm_line = ["// lt", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "D=M-D", f"@{label_1}", "D;JLT", "@SP", "A=M-1", "M=0", f"@{label_2}", "0;JMP", f"({label_1})", "@SP", "A=M-1", "M=-1", f"({label_2})"]
            self.ltNumber =  self.ltNumber + 1
            return asm_line
            
        elif command == "and":
            return ["// and", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=D&M"]
            
        elif command == "or":
            return ["// or", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=D|M"]
            
        elif command == "not":
            return ["// not", "@SP", "A=M-1", "M=!M"]
            
    
    def writePushPop(self, command, segment, index):
        asm_line = []
        if command == "push":
            if segment == "constant":
                asm_line = [f"// push constant {index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                asm_line.insert(1, f"@{index}")
                return asm_line
            elif segment in ["local", "argument", "this", "that", "R13", "R14", "R15"]:
                segment_name = SEGMENT_DICT[segment]
                if segment == "temp":
                    index = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", f"@{index}", "D=A", f"@{segment_name}", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                return asm_line
            elif segment == "temp":
                realIndex = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", f"@{realIndex}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                return asm_line
            elif segment == "pointer":
                if index == "0":
                    location = "THIS"
                elif index == "1":
                    location = "THAT"
                asm_line = [f"// {command} {segment} {index}", f"@{location}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                return asm_line
            elif segment == "static":
                staticLabel = f"{self.currentFile}.{index}"
                asm_line = [f"// {command} {segment} {index}", f"@{staticLabel}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                return asm_line
                

            
        if command == "pop":
            if segment in ["local", "argument", "this", "that", "R13", "R14", "R15"]:
                segment_name = SEGMENT_DICT[segment]
                if segment == "temp":
                    index = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", f"@{index}", "D=A", f"@{segment_name}", "D=M+D", "@R13", "M=D", "@SP", "M=M-1", "A=M", "D=M", "@R13", "A=M", "M=D"]
                return asm_line
            elif segment == "temp":
                realIndex = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", "@SP", "M=M-1", "A=M", "D=M", f"@{realIndex}", "M=D"]
                return asm_line
            elif segment == "pointer":
                if index == "0":
                    location = "THIS"
                elif index == "1":
                    location = "THAT"
                asm_line = [f"// {command} {segment} {index}", "@SP", "M=M-1", "A=M", "D=M", f"@{location}", "M=D"]
                return asm_line
            elif segment == "static":
                staticLabel = f"{self.currentFile}.{index}"
                asm_line = [f"// {command} {segment} {index}", "@SP", "M=M-1", "@SP", "A=M", "D=M", f"@{staticLabel}", "M=D"]
                return asm_line
    
    def close(self):
        return ["(END)", "@END", "0;JMP"]
    
    def writeLabel(self, label):
        final_label = f"{self.currentFunction}${label}"
        asm_line = [f"// writeLabel {final_label}", f"({final_label})"]
        return asm_line
        
    def writeGoto(self, label):
        final_label = f"{self.currentFunction}${label}"
        asm_line = [f"// writeGoto {final_label}", f"@{final_label}", "0;JMP"]
        return asm_line
        
    def writeIf(self, label):
        final_label = f"{self.currentFunction}${label}"
        asm_line = [f"// writeIf {final_label}", "@SP", "M=M-1", "@SP", "A=M", "D=M", f"@{final_label}", "D;JNE"]
        return asm_line
        
    def writeFunction(self, functionName, nVars):
        function_declaration = f"({functionName})"
        asm_line = [f"// writeFunction {self.currentFile}.{functionName} {nVars}", function_declaration]
        nVars_done = 0
        while nVars_done < int(nVars):
            asm_line.extend(["@0", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"])
            nVars_done = nVars_done + 1
        return asm_line
    
    def writeCall(self, functionName, nArgs):
        retAddr = f"{self.currentFunction}$ret.{self.retAddrCount}"
        self.retAddrCount = self.retAddrCount + 1
        asm_line = [f"// writeCall {self.currentFile}.{functionName} {nArgs}", 
                    f"@{retAddr}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                    "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                    "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                    "@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                    "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",
                    f"@{nArgs}", "D=A", "@5", "D=D+A", "@SP", "D=M-D", "@ARG", "M=D",
                    "@SP", "D=M", "@LCL", "M=D",
                    f"@{functionName}", "0;JMP",
                    f"({retAddr})"]
        return asm_line
        
        
        # call fileName.functionName nArgs
        # arg 0
        # ...
        # arg N (N = nArgs - 1)
        # push returnAddress
        # push LCL
        # push ARG
        # push THIS
        # push THAT
        # <prepping return>
        # ARG = SP-5-nArgs 
        # LCL=SP
        # goto fileName.functionName
        # (returnAddress)
    
    def writeReturn(self):
        # frame = LCL // frame = R13?
        # retAddr = A(frame-5) // frame = R14?
        # A(arg) = pop() // pop return value to top of stack
        # THAT =A(frame - 1)
        # THIS = A(frame - 2)
        # ARG = A(frame - 3)
        # LCL = A(frame - 4)
        # goto retAddr
        asm_line = ["// writeReturn", "@LCL", "D=M", "@R13", "M=D", 
                    "@5", "D=A", "@R13", "D=M-D", "A=D", "D=M", "@R14", "M=D",
                    "@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D", "@ARG", "D=M+1", "@SP", "M=D",
                    "@R13", "A=M-1", "D=M", "@THAT", "M=D",
                    "@2", "D=A", "@R13", "A=M-D", "D=M", "@THIS", "M=D",
                    "@3", "D=A", "@R13", "A=M-D", "D=M", "@ARG", "M=D",
                    "@4", "D=A", "@R13", "A=M-D", "D=M", "@LCL", "M=D",
                    "@R14", "A=M", "0;JMP"]
        return asm_line
                    
