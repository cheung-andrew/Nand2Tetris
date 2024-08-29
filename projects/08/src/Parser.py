import re 
from CodeWriter import CodeWriter

comment = re.compile("^\s*\/\/.*$")
comment2 = re.compile("^(.+)\/\/.*$")

COMMAND_DICT = {"add": "C_ARITHMETIC", "sub": "C_ARITHMETIC", "neg": "C_ARITHMETIC", "eq": "C_ARITHMETIC", "gt": "C_ARITHMETIC", "lt": "C_ARITHMETIC", "and": "C_ARITHMETIC", "or": "C_ARITHMETIC", "not": "C_ARITHMETIC", "push": "C_PUSH", "pop": "C_POP", "label": "C_LABEL", "goto": "C_GOTO", "if-goto": "C_IF", "function": "C_FUNCTION", "return": "C_RETURN", "call": "C_CALL"}


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
                if bool(comment2.match(cleaned_line)) == True:
                    cleaned_line = comment2.findall(cleaned_line)[0]
                    cleaned_line = cleaned_line.strip()
                cleanedFile.append(cleaned_line)
        return cleanedFile
    
    def hasMoreLines(self, file):
        return len(file) > 0
    
    def advance(self, currentCommand):
        command_type = self.commandType(currentCommand)
        if command_type in ["C_POP", "C_PUSH"]:
            command, segment, index = currentCommand.split()
            return self.codeWriter.writePushPop(command, segment, index)
        elif command_type == "C_ARITHMETIC":
            return self.codeWriter.writeArithmetic(currentCommand)
        elif command_type == "C_GOTO":
            return self.codeWriter.writeGoto(currentCommand.split()[1])
        elif command_type == "C_LABEL":
            return self.codeWriter.writeLabel(currentCommand.split()[1])
        elif command_type == "C_IF":
            return self.codeWriter.writeIf(currentCommand.split()[1])
        elif command_type == "C_FUNCTION":
            functionName, nVars = currentCommand.split()[1:]
            self.codeWriter.setCurrentFunction(functionName)
            return self.codeWriter.writeFunction(functionName, nVars)
        elif command_type == "C_RETURN":
            return self.codeWriter.writeReturn()
        elif command_type == "C_CALL":
            functionName, nArgs = currentCommand.split()[1:]
            return self.codeWriter.writeCall(functionName, nArgs)
            
            
        
        
    def commandType(self, command):
        first_word = command.split()[0]
        return COMMAND_DICT[first_word]
    
    #def arg1(self):
    
    #def arg2(self):