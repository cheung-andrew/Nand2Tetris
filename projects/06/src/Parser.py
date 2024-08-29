# parsing the input into instructions and instructions into fields
from Code import Code
from SymbolTable import SymbolTable
import re, logging
comment = re.compile("^\s*\/\/.*$")
blank = re.compile("^\s+$")
symbol = re.compile("^\((.+)\)")
C_INSTRUCTION_ELEMENTS = re.compile("(?:(M|D|MD|DM|A|AM|MA|AD|DA|ADM|AMD|MAD|MDA|DAM|DMA)=)?(0|1|\-1|\-D|\-A|\!D|\!A|\!M|D\+1|A\+1|M\+1|D\-1|A\-1|M\-1|D\+A|A\+D|D\+M|M\+D|D\-A|D\-M|A\-D|M\-D|D&A|A&D|D&M|M&D|D\|A|A\|D|D\|M|M\|D|D|A|M)(?:;(JGT|JEQ|JGE|JLT|JNE|JLE|JMP))?")

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

class Parser: 
    def __init__(self):
        self.code = Code()
        self.symbolTable = SymbolTable()
        self.symbolCounter = 16
        self.lineNumber = 0
    
    def reset(self):
        self.symbolCounter = 16
        self.lineNumber = 0
        self.symbolTable.reset()
        
    def buildSymbolTable(self, fileList):
        for line in fileList:
            
            if self.instructionType(line) in ["A_INSTRUCTION", "C_INSTRUCTION"]:
                self.lineNumber = self.lineNumber + 1
                continue
            if self.instructionType(line) == "L_INSTRUCTION":
                if self.symbolTable.contains(line[1:-1]) == True:
                    continue
                else:
                    label = line[1:-1]
                    self.symbolTable.addEntry(label, self.lineNumber)
                
    def hasMoreLines(self, fileList):
        return len(fileList) > 0
        
    def clean(self, fileList):
        cleanedFile = []
        for line in fileList:
            if bool(comment.match(line)) == True or line == "":
                continue
            else:
                cleaned_line = line.strip()
                cleanedFile.append(cleaned_line)
        return cleanedFile
    
    def advance(self, currentInstruction):
        instruction_type = self.instructionType(currentInstruction)
        if instruction_type == "A_INSTRUCTION":
            if currentInstruction[1].isnumeric() == True:
                a = int(currentInstruction[1:])
                return format(a, '016b')
            else:
                if  self.symbolTable.contains(currentInstruction[1:]) == False:
                    self.symbolTable.addEntry(currentInstruction[1:],self.symbolCounter)
                    self.symbolCounter = self.symbolCounter + 1
                    binary = self.symbolTable.getAddress(currentInstruction[1:])
                    return format(binary, '016b')
                else:
                    binary = self.symbolTable.getAddress(currentInstruction[1:])
                    return format(binary, '016b')


        elif instruction_type == "L_INSTRUCTION":
            return ""
            #return self.symbolTable.getAddress(currentInstruction[1:-1])
            
        else:
            match = C_INSTRUCTION_ELEMENTS.findall(currentInstruction)
            d, c, j = match[0]
            comp_bin = self.code.comp(c)
            dest_bin = self.code.dest(d)
            jump_bin = self.code.jump(j)
            return "111" + comp_bin + dest_bin + jump_bin
            
    
    def instructionType(self, currentInstruction):
        if currentInstruction[0] == "@":
            return "A_INSTRUCTION"
        elif currentInstruction[0] =="(" and currentInstruction[-1] == ")":
            return "L_INSTRUCTION"
        return "C_INSTRUCTION"
        
    #def symbol(self):
    