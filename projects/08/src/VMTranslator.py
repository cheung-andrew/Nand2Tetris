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
    fileName = pathlib.Path(path).name
    output = path / (fileName + ".asm")
    with open(output, 'w', encoding = 'utf-8') as o:
        #parsedFile = [["// bootstraping", "@SP", "D=A", "@SP", "M=D", "@Sys.init", "0;JMP", '(END)', '@END', '0;JMP']] 
        parsedFile = [['@256', 'D=A', '@SP', 'M=D', 
                       '@BEGINNING0000', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', 
                       '@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', 
                       '@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', 
                       '@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
                       '@THAT', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',                         
                       '@5', 'D=A', '@SP', 'D=M-D', '@ARG', 'M=D', '@SP', 'D=M', '@LCL', 'M=D', 
                       '@Sys.init', '0;JMP', 
                       '(BEGINNING0000)', 
                       '(END)', '@END', '0;JMP']]
        for file in filelist:
            print(str(parsedFile))
            with open(file) as f:
                parser.setCurrentFile(pathlib.Path(file).stem)
                originalFile = f.read().splitlines()
                originalFile = parser.clean(originalFile)
                
                while parser.hasMoreLines(originalFile):
                    currentCommand = originalFile.pop(0)
                    parsedFile.append(parser.advance(currentCommand))
                parser.close(parsedFile)
        for lineList in parsedFile:
            for line in lineList:
                o.write(f"{line}\n")
                