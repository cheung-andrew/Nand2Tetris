from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter
import re, pathlib, logging, sys
from Constants import *


logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

class CompilationEngine:

    def __init__(self, token_file):
        self.jackTokenizer = JackTokenizer()
        self.symbolTable = SymbolTable()
        self.vMWriter = VMWriter()
        self.token_file = token_file
        self.currentToken = self.token_file.pop(0)
        self.compiledFile = []
        self.current_class = ""
        self.subroutine_type_declared = ""
        self.return_type = ""
        self.nArgs = 0
        self.label_counter = 0
        self.function_name_declared = ""
        self.nVars = 0
        self.if_counter = 0
        self.string_counter = 0
        
    def write(self, vm_line):
        if isinstance(vm_line, list):
            for line in vm_line:
                self.compiledFile.append(line)
        else:
            self.compiledFile.append(vm_line)

        
    def setCurrentClass(self, class_name):
        self.current_class = class_name
    
    def getNextToken(self):
        if len(self.token_file) > 0:
            self.currentToken = self.token_file.pop(0)


    def process(self, string):

        if self.currentToken == string:
            # self.compiledFile.append(self.jackTokenizer.advance(string))
            #"KEYWORD", "STRING_CONST", "INT_CONST"
            if self.jackTokenizer.tokenType(string) == "INT_CONST":

                vm_line = self.vMWriter.writePush("constant", string)
                self.write(vm_line)
                self.getNextToken()
            elif self.jackTokenizer.tokenType(string) == "STRING_CONST":

                string_counter = self.string_counter
                self.string_counter = self.string_counter + 1
                string_length = len(string[1:-1])

                self.write(self.vMWriter.writePush("constant", string_length))
                self.write(self.vMWriter.writeCall("String.new", 1))
                for letter in string[1:-1]:

                    self.write(self.vMWriter.writePush("constant", CHAR_SET[letter]))
                    self.write(self.vMWriter.writeCall("String.appendChar", 2))
                self.getNextToken()
            elif string in keywordConstant:
                vm_line = []
                if string == "true":
                    vm_line.append(self.vMWriter.writePush("constant", 1))
                    vm_line.append(self.vMWriter.writeArithmetic("NEG"))
                
                elif string == "this":
                    vm_line.append(self.vMWriter.writePush("pointer", 0))
                
                else:
                    vm_line.append(self.vMWriter.writePush("constant", 0))
                self.write(vm_line)
                self.getNextToken()
            else:
                self.getNextToken()
            
        elif string in OP_MAP:

            vm_line = self.vMWriter.writeArithmetic(OP_MAP[string])
            self.write(vm_line)
        # elif string in UNARY_OP_MAP:
            # vm_line = self.vMWriter.writeArithmetic(UNARY_OP_MAP[string])
            # self.write(vm_line)
        elif string == "*":

            vm_line = self.vMWriter.writeArithmetic("MULTIPLY")
            self.write(vm_line)
        elif string == "/":
            vm_line = self.vMWriter.writeArithmetic("DIVIDE")
            self.write(vm_line)
        else:

            sys.exit(0)
        
    
    def compileClass(self):
        # self.compiledFile.append("<class>")
        self.process("class")
        self.compiling("className")
        self.process("{")
        while self.currentToken in ["static", "field"]:
            self.compileClassVarDec()

        nFields = self.symbolTable.varCount("field")
        self.vMWriter.setNFields(nFields)

        while self.currentToken in ["constructor", "function", "method"]:
            self.compileSubroutine()

        # self.process("}")
        # self.compiledFile.append("</class>")
        return self.compiledFile
        
        
    
    def compileClassVarDec(self):
        # self.compiledFile.append("<ClassVarDec>")
        var_kind = self.currentToken
        self.process(self.currentToken)
        var_type = self.currentToken
        self.compiling("type")
        var_name = self.currentToken
        self.symbolTable.define(var_name, var_type, var_kind)
        self.compiling("varName")
        while self.currentToken == ",":
            self.process(",")
            var_name = self.currentToken
            self.symbolTable.define(var_name, var_type, var_kind)
            self.compiling("varName")
        self.process(";")
        # self.compiledFile.append("</ClassVarDec>")
    
    def compileSubroutine(self):

        # self.compiledFile.append("<subroutineDec>")
        
        self.symbolTable.reset()
        if self.currentToken == "method":

            self.symbolTable.define("this", self.current_class, "arg")

        self.vMWriter.setSubroutineTypeDeclared(self.currentToken)
        self.subroutine_type_declared = self.currentToken
        self.process(self.currentToken)

        self.return_type = self.currentToken
        self.vMWriter.setReturnType(self.currentToken)
        self.return_type = self.currentToken
        self.compiling("returnType")
        self.function_name_declared = f"{self.current_class}.{self.currentToken}"
        self.compiling("subroutineName")
        self.process("(")
        self.compileParameterList()
        self.process(")")

        # compileExpressionList first before calling function
        self.compileSubroutineBody()
        # self.compiledFile.append("</subroutineDec>")
    
    def compileParameterList(self):
        # self.compiledFile.append("<parameterList>")
        if self.currentToken != ")":
            var_kind = "arg"
            var_type = self.currentToken
            self.compiling("type")
            var_name = self.currentToken
            self.symbolTable.define(var_name, var_type, var_kind)
            self.compiling("varName")
            while self.currentToken == ",":
                self.process(",")
                var_type = self.currentToken
                self.compiling("type")
                var_name = self.currentToken
                self.symbolTable.define(var_name, var_type, var_kind)
                self.compiling("varName")
        # self.compiledFile.append("</parameterList>")
    
    # To simplify things, the following Jack grammar rules are not accounted for explicitly in the XML output: type, className, subroutineName, varName, statement, subroutineCall
    
    def compiling(self, unaccounted_type):
        if unaccounted_type in ["type", "returnType", "subroutineName", "varName"]:
            self.process(self.currentToken)
        if unaccounted_type == "className":
            if self.currentToken != self.current_class:

                sys.exit(0)
            else:
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
            self.nArgs = 0
            if next_token != ".":
                # if it is a bare subroutine call, it is a method call of current class
                varName_called = self.current_class
                whole_function_called = f"{varName_called}.{self.currentToken}"

                self.compiling("subroutineName")
                self.write(self.vMWriter.writePush("pointer", 0))
                self.nArgs = 1
                
            else:
                #var_name = self.currentToken
                #self.symbolTable.getVar(var_name)
                varName_called = self.currentToken
                self.compiling("varName")
                self.process(".")
                function_called = self.currentToken
                whole_function_called = f"{varName_called}.{function_called}"
                self.compiling("subroutineName")
                # if varName_called found in symbolTable, it is a method call 
                if self.symbolTable.getVar(varName_called) == True: 

                    var_kind = self.symbolTable.kindOf(varName_called)
                    var_index = self.symbolTable.indexOf(varName_called)
                    self.write(self.vMWriter.writePush(var_kind, var_index))
                    class_name_called = self.symbolTable.typeOf(varName_called)
                    whole_function_called = f"{class_name_called}.{function_called}"
                    self.nArgs = 1

            # checking if it is function or method
            # if varName_called found in symbolTable, or no varName_called is given, then is method

            self.process("(")
            self.compileExpressionList()
            self.process(")")

            vm_line = self.vMWriter.writeCall(whole_function_called, self.nArgs)

            if vm_line != None:
                self.write(vm_line)
            
    def compileSubroutineBody(self):
        # self.compiledFile.append("<subroutineBody>")
        self.process("{")
        while self.currentToken == "var":

            self.compileVarDec()
        self.nVars = self.symbolTable.varCount("local")
        vm_line = self.vMWriter.writeFunction(self.function_name_declared, self.nVars)
        self.write(vm_line)
        self.compileStatements()
        self.process("}")
        # self.compiledFile.append("</subroutineBody>")

    def compileVarDec(self):
        # self.compiledFile.append("<varDec>")
        self.process(self.currentToken)
        var_type = self.currentToken
        self.compiling("type")
        var_name = self.currentToken
        self.symbolTable.define(var_name, var_type, "local")
        self.compiling("varName")
        while self.currentToken == ",":
            self.process(",")
            var_name = self.currentToken
            self.symbolTable.define(var_name, var_type, "local")
            self.compiling("varName")
        self.process(";")
        # self.compiledFile.append("</varDec>")
    
    def compileStatements(self):
        # self.compiledFile.append("<statements>")

        while self.currentToken in ["let", "if", "while", "do", "return"]:
            self.compiling("statement")
        # self.compiledFile.append("</statements>")
    
    def compileLet(self):
        # self.compiledFile.append("<letStatement>")
        self.process("let")

        var_name = self.currentToken
        next_token = self.token_file[0]
        if next_token == "[":

            var_kind = self.symbolTable.kindOf(var_name)
            var_index = self.symbolTable.indexOf(var_name)
            self.write(self.vMWriter.writePush(var_kind, var_index))
            
            self.symbolTable.getVar(var_name)
            self.process(self.currentToken)
            self.process("[")
            self.compileExpression()
            self.process("]")
            self.write(self.vMWriter.writeArithmetic("ADD"))
            self.process("=")
            self.compileExpression()
            self.write(self.vMWriter.writePop("temp", 0))
            self.write(self.vMWriter.writePop("pointer", 1))
            self.write(self.vMWriter.writePush("temp", 0))
            self.write(self.vMWriter.writePop("that", 0))      
            self.process(";")

        # if self.currentToken == "[":
            # self.process("[")
            # self.compileExpression()
            # self.process("]")
        else: 
            self.compiling("varName")
            self.process("=")
            self.compileExpression()
            var_kind = self.symbolTable.kindOf(var_name)
            var_index = self.symbolTable.indexOf(var_name)
            vm_line = self.vMWriter.writePop(var_kind, var_index)
            self.write(vm_line)
            self.process(";")
        # self.compiledFile.append("</letStatement>")

    
    def compileIf(self):
        # self.compiledFile.append("<ifStatement>")

        self.process("if")
        self.process("(")
        self.compileExpression()
        if_counter = self.if_counter
        self.if_counter = self.if_counter + 1
        if_true_label = f"IF_TRUE_{if_counter}"
        if_not_true_label = f"IF_NOT_TRUE_{if_counter}"
        self.write(self.vMWriter.writeArithmetic("NOT"))
        self.write(self.vMWriter.writeIf(if_not_true_label))
        self.process(")")
        self.process("{")
        self.compileStatements()
        self.process("}")
        self.write(self.vMWriter.writeGoto(if_true_label))
        self.write(self.vMWriter.writeLabel(if_not_true_label))
        if self.currentToken == "else":
            self.process("else")
            self.process("{")
            self.compileStatements()
            self.process("}")
        self.write(self.vMWriter.writeLabel(if_true_label))
        # self.compiledFile.append("</ifStatement>")
        
    def compileWhile(self):
        # self.compiledFile.append("<whileStatement>")

        self.process("while")
        if_counter = self.if_counter
        self.if_counter = self.if_counter + 1
        while_true_label = f"WHILE_TRUE_{if_counter}"
        while_not_true_label = f"WHILE_NOT_TRUE_{if_counter}"
        self.write(self.vMWriter.writeLabel(while_true_label))
        self.process("(")
        self.compileExpression()
        self.process(")")
        self.write(self.vMWriter.writeArithmetic("NOT"))
        self.write(self.vMWriter.writeIf(while_not_true_label))        
        self.process("{")
        self.compileStatements()
        self.write(self.vMWriter.writeGoto(while_true_label))
        self.process("}")
        self.write(self.vMWriter.writeLabel(while_not_true_label))
        # self.compiledFile.append("</whileStatement>")
        
    def compileDo(self):
        # self.compiledFile.append("<doStatement>")

        self.process("do")
        self.compiling("subroutineCall")
        self.write("pop temp 0")
        self.process(";")
        # self.compiledFile.append("</doStatement>")
        
    def compileReturn(self):
        # self.compiledFile.append("<returnStatement>")

        self.process("return")
        if self.return_type == "void":
            self.write(self.vMWriter.writePush("constant", 0))
        elif self.jackTokenizer.tokenType(self.currentToken) in ["INT_CONST", "STRING_CONST", "KEYWORD", "IDENTIFIER"] or self.currentToken in ["(", "-", "~"]:
            self.compileExpression()
        # else: 
            # self.write("push constant 0")
        self.write("return")
        self.process(";")
        # self.compiledFile.append("</returnStatement>")
        
    def compileExpression(self):
        # self.compiledFile.append("<expression>")

        # self.compileTerm()
        # while self.currentToken in op:
            # self.process(self.currentToken)
            # self.compileTerm()
        self.compileTerm()
        while self.currentToken in op:

            current_op = self.currentToken
            self.getNextToken()
            self.compileTerm()
            self.process(current_op)

        # while self.jackTokenizer.tokenType(self.currentToken) in ["INT_CONST",  "STRING_CONST", "IDENTIFIER"] or self.currentToken in keywordConstant or self.currentToken in unaryOp or self.currentToken == "(":
            # whole_expression.append(self.currentToken)
            # self.getNextToken()
        # self.compiledFile.append("</expression>")
    
    def compileTerm(self):
        # self.compiledFile.append("<term>")

        if self.jackTokenizer.tokenType(self.currentToken) in ["STRING_CONST", "INT_CONST"] or self.currentToken in keywordConstant:
            self.process(self.currentToken)
        elif self.currentToken == "(":
            self.process("(")
            self.compileExpression()
            self.process(")")
        elif self.currentToken in unaryOp:
            current_unaryOp = self.currentToken
            self.getNextToken()
            self.compileTerm()
            vm_line = self.vMWriter.writeArithmetic(UNARY_OP_MAP[current_unaryOp])
            self.write(vm_line)
        elif self.jackTokenizer.tokenType(self.currentToken) == "IDENTIFIER":
            next_token = self.token_file[0]
            if next_token == "[":

                var_name = self.currentToken
                var_kind = self.symbolTable.kindOf(var_name)
                var_index = self.symbolTable.indexOf(var_name)
                self.write(self.vMWriter.writePush(var_kind, var_index))
                
                self.symbolTable.getVar(var_name)
                self.process(self.currentToken)
                self.process("[")
                self.compileExpression()
                self.process("]")
                self.write(self.vMWriter.writeArithmetic("ADD"))
                self.write(self.vMWriter.writePop("pointer", 1))
                self.write(self.vMWriter.writePush("that", 0))
            elif next_token == ".":
                self.compiling("subroutineCall")
            else:
                # compiling var_name usage
                var_name = self.currentToken
                var_kind = self.symbolTable.kindOf(var_name)
                var_index = self.symbolTable.indexOf(var_name)
                vm_line = self.vMWriter.writePush(var_kind, var_index)
                self.write(vm_line)
                self.getNextToken()
        # self.compiledFile.append("</term>")
        
    
    def compileExpressionList(self):
        # self.compiledFile.append("<expressionList>")

        if self.currentToken != ")":
            self.nArgs = self.nArgs + 1
            self.compileExpression()
            while self.currentToken == ",":
                self.process(",")
                self.nArgs = self.nArgs + 1
                self.compileExpression()
        # self.compiledFile.append("</expressionList>")