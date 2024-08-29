import sys, re, os, pathlib, logging
from Parser import Parser

parser = Parser()
hack = re.compile("^(.+)\.asm")
isHack = False
path = pathlib.Path.cwd()

def assemble(path, file):
    output = path / (pathlib.Path(file).stem + ".hack")
    with open(output, 'w', encoding = 'utf-8') as o:
        with open((file))as f:
            originalFile = f.read().splitlines()
            originalFile = parser.clean(originalFile)
            parsedFile = []
            parser.reset()
            parser.buildSymbolTable(originalFile)               
            
            while parser.hasMoreLines(originalFile):
                currentInstruction = originalFile.pop(0)
                parsedFile.append(parser.advance(currentInstruction))
                parsedFile = list(filter(None, parsedFile))
            for line in parsedFile:
                o.write(f"{line}\n")

if len(sys.argv) > 1: # if more than 1 arg given 
    if bool(hack.match(sys.argv[1])) == True: # if a jack file given
        isHack = True
        path = pathlib.Path(sys.argv[1]).parent.resolve()
        assemble(path, sys.argv[1])
    else:
        path = pathlib.Path(sys.argv[1]).resolve() # a path given 
        
### translating jack files in a folder 
if isHack == False: 
    filelist = list(pathlib.Path(path).glob('*.asm'))
    for file in filelist:
        assemble(path, file)



# parse instruction into fields
# for each field, gen bit codes







# if symbolic ref, resolve to no.
# get 16 bits
# write to output 
# no symbolic ref, then ys 
# symbols:
# create a symbol table
# init with predefined symbols and their values
# 1st pass: 
# - track line no., increment when A or C instruction is found
# - when label (xxx), add xxx and next line no. to table 
# 2nd pass:
# - when A instruction with symbolic ref @xxx, resolve
# - if the ref is not found, add xxx and next available RAM addr to table (>15)


