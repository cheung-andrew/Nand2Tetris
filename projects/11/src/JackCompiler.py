import sys, re, pathlib, logging, os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

jackTokenizer = JackTokenizer()
jack = re.compile("^(.+)\.jack")
isJack = False
path = pathlib.Path.cwd()

def compileJack(path, file):
    compilationEngine_output = path / (pathlib.Path(file).stem + ".vm")
    print(f"doing compileJack: {path}, {file}")
    print(f"compilationEngine_output = {compilationEngine_output}")
    with open(compilationEngine_output, 'w', encoding = 'utf-8') as p:
        with open((file))as f:
            originalFile = f.read().splitlines()
            originalFile = jackTokenizer.clean(originalFile)
            compilationEngine = CompilationEngine(originalFile)
            compilationEngine.setCurrentClass(pathlib.Path(file).stem)
            compiledFile = compilationEngine.compileClass()
            for line in compiledFile:
                p.write(f"{line}\n")

if len(sys.argv) > 1: # if more than 1 arg given 
    if bool(jack.match(sys.argv[1])) == True: # if a jack file given
        isJack = True
        path = pathlib.Path(sys.argv[1]).parent.resolve()
        compileJack(path, sys.argv[1])
    else:
        path = pathlib.Path(sys.argv[1]).resolve() # a path given 
        
### translating jack files in a folder 
if isJack == False: 
    filelist = list(pathlib.Path(path).glob('*.jack'))
    for file in filelist:
        compileJack(path, file)