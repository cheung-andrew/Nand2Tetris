import logging, re, pathlib, sys
from Parser import Parser


path = pathlib.Path.cwd()
vmfile = re.compile("^(.+)\.vm")
isFile = False
parser = Parser()


def translate(path, file):
    output = path / (pathlib.Path(file).stem + ".asm")
    with open(output, 'w', encoding = 'utf-8') as o:
        with open((file))as f:
            parser.setCurrentFile(pathlib.Path(file).stem)
            originalFile = f.read().splitlines()
            originalFile = parser.clean(originalFile)
            parsedFile = []             
            
            while parser.hasMoreLines(originalFile):
                currentCommand = originalFile.pop(0)
                parsedFile.append(parser.advance(currentCommand))
            parser.close(parsedFile)
            for lineList in parsedFile:
                for line in lineList:
                    o.write(f"{line}\n")

if len(sys.argv) > 1: # if more than 1 arg given 
    if bool(vmfile.match(sys.argv[1])) == True: # if a jack file given
        isHack = True
        path = pathlib.Path(sys.argv[1]).parent.resolve()
        translate(path, sys.argv[1])
    else:
        path = pathlib.Path(sys.argv[1]).resolve() # a path given 
        
### translating jack files in a folder 
if isFile == False: 
    filelist = list(pathlib.Path(path).glob('*.vm'))
    for file in filelist:
        translate(path, file)