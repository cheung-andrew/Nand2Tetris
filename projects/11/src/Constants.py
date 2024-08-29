import re
comment = re.compile("^\s*\/\/.*$")
commentTrail = re.compile("^(.+)\/\/.*$")
commenting = re.compile(r'^(\s+)?/\*.*')
commentingEnd = re.compile(r'.*\*/(.*)?')
identifierRG = re.compile(r'^[^0-9]{1}[0-9a-zA-Z_]*$')
CONSTRUCTOR_RE = re.compile(r'^\w+\.new\s[0-9]+$')

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
keywordConstant = {"true", "false", "null", "this"}

OP_MAP = {"+": "ADD", "-": "SUB", "=": "EQ", ">": "GT", "<": "LT", "&": "AND", "|": "OR"}
UNARY_OP_MAP = {"-": "NEG", "~": "NOT"}

WRITE_MEMORY_MAP = {"static": "static", "field": "this", "arg": "argument", "local": "local", "pointer": "pointer", "temp": "temp", "that": "that"}
WRITE_ARITHMETIC_MAP = {"ADD": "add", "SUB": "sub", "NEG": "neg", "EQ": "eq", "GT": "gt", "LT": "lt", "AND": "and", "OR": "or", "NOT": "not"}

CHAR_SET = {" ": 32, "!": 33, '"': 34, "#": 35, "$": 36, "%": 37, "&": 38, "'": 39, "(": 40, ")": 41, "*": 42, "+": 43, ",": 44, "-": 45, ".": 46, "/": 47, "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, ":": 58, ";": 59, "<": 60, "=": 61, ">": 62, "?": 63, "@": 64, "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "[": 91, "/": 92, "]": 93, "^": 94, "_": 95, "`": 96, "a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103, "h": 104, "i": 105, "j": 106, "k": 107, "l": 108, "m": 109, "n": 110, "o": 111, "p": 112, "q": 113, "r": 114, "s": 115, "t": 116, "u": 117, "v": 118, "w": 119, "x": 120, "y": 121, "z": 122, "{": 123, "|": 124, "}": 125, "~": 126}