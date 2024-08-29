import re
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

