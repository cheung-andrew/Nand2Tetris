from JackTokenizer import JackTokenizer
import re, pathlib, logging, sys
from Constants import *

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

class CompilationEngine:

    def __init__(self, token_file):
        self.jackTokenizer = JackTokenizer()
        self.token_file = token_file
        self.currentToken = self.token_file.pop(0)
        self.compiledFile = []
        print(str(self.currentToken))
        print(str(self.token_file))
        
    
    def getNextToken(self):
        if len(self.token_file) > 0:
            self.currentToken = self.token_file.pop(0)
            #print(f"The current Token is {self.currentToken}.\n")

    def process(self, string):
        print(f"doing process {string}")
        if self.currentToken == string:
            
            #print(str(string))
            self.compiledFile.append(self.jackTokenizer.advance(string))
            #print(f"finished processing {string}, the token_file is {self.token_file}.\n")
            self.getNextToken()
            #print(f"finished getNextToken, the token_file is {self.token_file}.\n")
        else:
            #print(str(self.token_file[1:]))
            print("syntax error")
            sys.exit(0)
        
    
    def compileClass(self):
        self.compiledFile.append("<class>")
        self.process("class")
        print(f"Finished processing class.")
        self.compiling("className")
        print(f"finish compiling className")
        self.process("{")
        while self.currentToken in ["static", "field"]:
            self.compileClassVarDec()
        print(f"finish compileClassVarDec")
        while self.currentToken in ["constructor", "function", "method"]:
            self.compileSubroutine()
        print(f"finish compileSubroutine")
        self.process("}")
        self.compiledFile.append("</class>")
        return self.compiledFile
        
        
    
    def compileClassVarDec(self):
        self.compiledFile.append("<ClassVarDec>")
        self.process(self.currentToken)
        self.compiling("type")
        self.compiling("varName")
        while self.currentToken == ",":
            self.process(",")
            self.compiling("varName")
        self.process(";")
        self.compiledFile.append("</ClassVarDec>")
    
    def compileSubroutine(self):
        print(f"doing compileSubroutine")
        self.compiledFile.append("<subroutineDec>")
        print(f"the subroutine type is {self.currentToken}")
        self.process(self.currentToken)
        self.compiling("returnType")
        print(f"the subroutine name is {self.currentToken}")
        self.compiling("subroutineName")
        self.process("(")
        self.compileParameterList()
        print(f"finished compileParameterList")
        self.process(")")
        self.compileSubroutineBody()
        self.compiledFile.append("</subroutineDec>")
    
    def compileParameterList(self):
        self.compiledFile.append("<parameterList>")
        if self.currentToken != ")":
            self.compiling("type")
            self.compiling("varName")
            while self.currentToken == ",":
                self.process(",")
                self.compiling("type")
                self.compiling("varName")
        self.compiledFile.append("</parameterList>")
    
    # To simplify things, the following Jack grammar rules are not accounted for explicitly in the XML output: type, className, subroutineName, varName, statement, subroutineCall
    
    def compiling(self, unaccounted_type):
        if unaccounted_type in ["type", "returnType", "className", "subroutineName", "varName"]:
            #print(f"compiling {unaccounted_type}, calling process")
            self.process(self.currentToken)

        elif unaccounted_type == "statement":
            if self.currentToken == "let":
                self.compileLet()
            elif self.currentToken == "if":
                self.compileIf()
            elif self.currentToken == "while":
                self.compileWhile()
            elif self.currentToken == "do":
                self.compileDo()
            elif self.currentToken == "return":
                self.compileReturn()
        elif unaccounted_type == "subroutineCall":
            next_token = self.token_file[0]
            if next_token == ".":
                self.compiling("varName")
                self.process(".")
                self.compiling("subroutineName")
            else:
                self.compiling("subroutineName")
            self.process("(")
            self.compileExpressionList()
            self.process(")")
            
    def compileSubroutineBody(self):
        self.compiledFile.append("<subroutineBody>")
        self.process("{")
        while self.currentToken == "var":
            self.compileVarDec()
        print(f"finished compileVarDec")
        self.compileStatements()
        self.process("}")
        self.compiledFile.append("</subroutineBody>")

    def compileVarDec(self):
        self.compiledFile.append("<varDec>")
        self.process(self.currentToken)
        self.compiling("type")
        self.compiling("varName")
        while self.currentToken == ",":
            self.process(",")
            self.compiling("varName")
        self.process(";")
        self.compiledFile.append("</varDec>")
    
    def compileStatements(self):
        self.compiledFile.append("<statements>")
        while self.currentToken in ["let", "if", "while", "do", "return"]:
            print(f"doing compiling statement {self.currentToken}")
            self.compiling("statement")
        self.compiledFile.append("</statements>")
    
    def compileLet(self):
        self.compiledFile.append("<letStatement>")
        self.process("let")
        print(f"compiling compileLet. The varName is {self.currentToken}")
        self.compiling("varName")
        if self.currentToken == "[":
            self.process("[")
            self.compileExpression()
            self.process("]")
        self.process("=")
        self.compileExpression()
        self.process(";")
        self.compiledFile.append("</letStatement>")
        print(f"finished compileLet")
    
    def compileIf(self):
        self.compiledFile.append("<ifStatement>")
        self.process("if")
        self.process("(")
        self.compileExpression()
        self.process(")")
        self.process("{")
        self.compileStatements()
        print(f"finished if in compileIf")
        self.process("}")
        if self.currentToken == "else":
            print(f"compiling else in compileIf")
            self.process("else")
            self.process("{")
            self.compileStatements()
            self.process("}")
        self.compiledFile.append("</ifStatement>")
        
    def compileWhile(self):
        self.compiledFile.append("<whileStatement>")
        self.process("while")
        self.process("(")
        self.compileExpression()
        self.process(")")
        self.process("{")
        self.compileStatements()
        self.process("}")
        self.compiledFile.append("</whileStatement>")
        
    def compileDo(self):
        self.compiledFile.append("<doStatement>")
        self.process("do")
        self.compiling("subroutineCall")
        self.process(";")
        self.compiledFile.append("</doStatement>")
        
    def compileReturn(self):
        self.compiledFile.append("<returnStatement>")
        self.process("return")
        if self.jackTokenizer.tokenType(self.currentToken) in ["INT_CONST", "STRING_CONST", "KEYWORD", "IDENTIFIER"] or self.currentToken in ["(", "-", "~"]:
            self.compileExpression()
        self.process(";")
        self.compiledFile.append("</returnStatement>")
        
    def compileExpression(self):
        print(f"doing compileExpression")
        self.compiledFile.append("<expression>")
        self.compileTerm()
        while self.currentToken in op:
            print(f"Found an op in compileExpression. The op is {self.currentToken}. The next token is {self.token_file[0]}")
            self.process(self.currentToken)
            print(f"finished process op in compileExpression")
            self.compileTerm()
        self.compiledFile.append("</expression>")
    
    def compileTerm(self):
        print(f"doing compileTerm. The term is {self.currentToken}")
        self.compiledFile.append("<term>")
        if self.jackTokenizer.tokenType(self.currentToken) in ["KEYWORD", "STRING_CONST", "INT_CONST"]:
            self.process(self.currentToken)
        elif self.currentToken == "(":
            print(f"doing compileTerm. Found an (")
            self.process("(")
            self.compileExpression()
            self.process(")")
        elif self.currentToken in unaryOp:
            self.process(self.currentToken)
            self.compileTerm()
        elif self.jackTokenizer.tokenType(self.currentToken) == "IDENTIFIER":
            next_token = self.token_file[0]
            if next_token == "[":
                self.process(self.currentToken)
                self.process("[")
                self.compileExpression()
                self.process("]")
            elif next_token == ".":
                self.compiling("subroutineCall")
            else:
                self.compiling("varName")
        self.compiledFile.append("</term>")
        
    
    def compileExpressionList(self):
        self.compiledFile.append("<expressionList>")
        while self.currentToken != ")":
            self.compileExpression()
            while self.currentToken == ",":
                self.process(",")
                self.compileExpression()
        self.compiledFile.append("</expressionList>")