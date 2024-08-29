import re
from Constants import *

comment = re.compile("^\s*\/\/.*$")
commentTrail = re.compile("^(.+)\/\/.*$")
commenting = re.compile(r'^(\s+)?/\*.*')
commentingEnd = re.compile(r'.*\*/(.*)?')
identifierRG = re.compile(r'^[^0-9]{1}[0-9a-zA-Z_]*$')

checkTokens = re.compile(r'^\s*(\bclass\b|\bconstructor\b|\bfunction\b|\bmethod\b|\bfield\b|\bstatic\b|\bvar\b|\bint\b|\bchar\b|\bboolean\b|\bvoid\b|\btrue\b|\bfalse\b|\bnull\b|\bthis\b|\blet\b|\bdo\b|\bif\b|\belse\b|\bwhile\b|\breturn\b|\b\d{1,4}\b|\b[12]\d{4}\b|\b3[01]\d{3}\b|\b32[0-6]\d{2}\b|\b327[0-5]\d\b|\b3276[0-7]\b|\(|\)|\{|\}|\[|\]|\.|,|;|\+|\-|\*|/|&|\||<|>|=|~|".+"|\b[a-zA-Z_][a-zA-Z0-9_]*\b)(.*)$')

keywords = ["class", "constructor", "function", "method", 
            "field", "static", "var", "int", "char",
            "boolean", "void", "true", "false", "null", 
            "this", "let", "do", "if", "else", "while", 
            "return"]

            
symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
            "+", "-", "*", "/", "&", "|", "<", ">", "=",
            "~"]
specialSymbols = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}

typeKeywords = ["int", "char", "boolean"]
subroutineDecKeywords = ["constructor", "function", "method"]
statementKeywords = ["let", "if", "while", "do", "return"]
op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unaryOp = ["-", "~"]
keywordConstant = ["true", "false", "null", "this"] 

class JackTokenizer:

    def __init__(self):
        self.commenting = False

    def clean(self, fileList):
        token_list = []
        for line in fileList:
            if bool(comment.match(line)) == True or line == "":
                continue
            elif bool(commenting.match(line)) == True or self.commenting == True:
                if bool(commentingEnd.match(line)) == False:
                    self.commenting = True
                    continue
                else:
                    self.commenting = False
                    continue
            else:
                cleaned_line = line.strip()
                if bool(commentTrail.match(cleaned_line)) == True:
                    cleaned_line = commentTrail.findall(cleaned_line)[0]
                    cleaned_line = cleaned_line.strip()
                ## getting individual tokens 
                while bool(checkTokens.match(cleaned_line)) == True:
                    new_token, cleaned_line = checkTokens.findall(cleaned_line)[0]
                    token_list.append(new_token)
        return token_list

    def hasMoreTokens(self, originalFile):
        return len(originalFile) > 0
    
    def advance(self, currentToken):
        token_type = self.tokenType(currentToken)
        if token_type == "KEYWORD":
            token_modified = self.keyWord(currentToken)
        elif token_type == "SYMBOL":
            token_modified = self.symbol(currentToken)
        elif token_type == "INT_CONST":
            token_modified = self.intVal(currentToken)
        elif token_type == "STRING_CONST":
            token_modified = self.stringVal(currentToken)
        elif token_type == "IDENTIFIER":
            token_modified = self.identifier(currentToken)
        token_type_returning = self.returnTokenType(token_type)
        return f"<{token_type_returning}> {token_modified} </{token_type_returning}>"
            
    def returnTokenType(self, token_type):
        if token_type == "INT_CONST":
            return "integerConstant"
        elif token_type == "STRING_CONST":
            return "stringConstant"
        else:
            return token_type.lower()
    
    def tokenType(self, currentToken):
        if currentToken in keywords: 
            return "KEYWORD"
        elif currentToken in symbols:
            return "SYMBOL"
        elif str(currentToken).isnumeric():
            return "INT_CONST"
        elif currentToken.startswith('"') and currentToken.endswith('"'):
            return "STRING_CONST"
        elif bool(identifierRG.match(currentToken)) == True:
            return "IDENTIFIER"
    
    def keyWord(self, currentToken):
        return currentToken
        
    def symbol(self, currentToken):
        if currentToken in specialSymbols:
            return specialSymbols[currentToken]
        return currentToken
    
    def identifier(self, currentToken):
        return currentToken
    
    def intVal(self, currentToken):
        return currentToken
        
    def stringVal(self, currentToken):
        return currentToken[1:-1]