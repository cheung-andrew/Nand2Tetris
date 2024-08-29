import sys, re, pathlib, logging
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

jackTokenizer = JackTokenizer()
jack = re.compile("^(.+)\.jack")
isJack = False
path = pathlib.Path.cwd()

def compile(path, file):
    tokenizer_output = path / (pathlib.Path(file).stem + "T.xml")
    compilationEngine_output = path / (pathlib.Path(file).stem + ".xml")
    with open(tokenizer_output, 'w', encoding = 'utf-8') as o:
        with open(compilationEngine_output, 'w', encoding = 'utf-8') as p:
            with open((file))as f:
                originalFile = f.read().splitlines()
                originalFile = jackTokenizer.clean(originalFile)
                compilationEngine = CompilationEngine(originalFile)
                tokenizedFile = ["<tokens>"]
                compiledFile = compilationEngine.compileClass()
                
                while jackTokenizer.hasMoreTokens(originalFile):
                    currentToken = originalFile.pop(0)
                    tokenizedFile.append(jackTokenizer.advance(currentToken))
                    tokenizedFile = list(filter(None, tokenizedFile))
                tokenizedFile.append("</tokens>")
                #for line in tokenizedFile:
                    #o.write(f"{line}\n")
                for line in compiledFile:
                    p.write(f"{line}\n")

if len(sys.argv) > 1: # if more than 1 arg given 
    if bool(jack.match(sys.argv[1])) == True: # if a jack file given
        isJack = True
        path = pathlib.Path(sys.argv[1]).parent.resolve()
        compile(path, sys.argv[1])
    else:
        path = pathlib.Path(sys.argv[1]).resolve() # a path given 
        
### translating jack files in a folder 
if isJack == False: 
    filelist = list(pathlib.Path(path).glob('*.jack'))
    for file in filelist:
        compile(path, file)