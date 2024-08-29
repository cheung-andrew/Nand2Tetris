import re 
from CodeWriter import CodeWriter

comment = re.compile("^\s*\/\/.*$")

class Parser:
    def __init__(self):
        self.codeWriter = CodeWriter()
        self.addrMap = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, 
                        "TEMP": 5, "R13": 13, "R14": 14, "R15": 15,
                        "static": 256}
        self.currentFile = ""
        
    def setCurrentFile(self, file_name):
        self.currentFile = file_name
        self.codeWriter.setCurrentFile(file_name)
        
    def close(self, parsedFile):
        parsedFile.append(self.codeWriter.close())
        
    def clean(self, fileList):
        cleanedFile = []
        for line in fileList:
            if bool(comment.match(line)) == True or line == "":
                continue
            else:
                cleaned_line = line.strip()
                cleanedFile.append(cleaned_line)
        return cleanedFile
    
    def hasMoreLines(self, file):
        return len(file) > 0
    
    def advance(self, currentCommand):
        command_type = self.commandType(currentCommand)
        if command_type in ["C_POP", "C_PUSH"]:
            command, segment, index = currentCommand.split()
            print(f"{command} {segment} {index}")
            return self.codeWriter.writePushPop(command, segment, index)
        elif command_type == "C_ARITHMETIC":
            return self.codeWriter.writeArithmetic(currentCommand)
        
        
    def commandType(self, command):
        first_word = command.split()[0]
        print(str(first_word))
        if first_word in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif first_word == "push":
            print("its push")
            return "C_PUSH"
            
        elif first_word == "pop":
            return "C_POP"
        #C_LABEL
        #C_GOTO
        #C_IF
        #C_FUNCTION
        #C_RETURN
        #C_CALL
    
    #def arg1(self):
    
    #def arg2(self):