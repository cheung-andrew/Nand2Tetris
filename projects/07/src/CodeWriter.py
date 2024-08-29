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
        
        
    def setCurrentFile(self, file_name):
        self.currentFile = file_name
    
    def writeArithmetic(self, command):
        if command == "add":
            return ["// add", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=D+M"]
        elif command == "sub":
            return ["// sub", "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=M-D"]
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
            print("lets write push")
            if segment == "constant":
                print(str("its push constant!"))
                asm_line = [f"// push constant {index}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
                asm_line.insert(1, f"@{index}")
                return asm_line
            elif segment in ["local", "argument", "this", "that", "temp", "R13", "R14", "R15"]:
                segment_name = SEGMENT_DICT[segment]
                if segment == "temp":
                    index = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", f"@{index}", "D=A", f"@{segment_name}", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
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
            if segment in ["local", "argument", "this", "that", "temp", "R13", "R14", "R15"]:
                segment_name = SEGMENT_DICT[segment]
                if segment == "temp":
                    index = int(index) + 5
                asm_line = [f"// {command} {segment} {index}", f"@{index}", "D=A", f"@{segment_name}", "D=M+D", "@R13", "M=D", "@SP", "M=M-1", "A=M", "D=M", "@R13", "A=M", "M=D"]
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
                asm_line = [f"// {command} {segment} {index}", "@SP", "M=M-1", "A=M", "D=M", f"@{staticLabel}", "M=D"]
                return asm_line
    
    def close(self):
        return ["(END)", "@END", "0;JMP"]
    
    def writeLabel(self, label):
    
    
    def writeGoto(self, label):
    
    def writeIf(self, label):
    
    def writeFunction(self, functionName, nVars):
    
    def writeCall(self, functionName, nArgs):
    
    def writeReturn(self):
