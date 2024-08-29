// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@0
D=A
@THAT
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@1
D=A
@THAT
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// pop argument 0
@0
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// writeLabel FibonacciSeries$MAIN_LOOP_START
(FibonacciSeries$MAIN_LOOP_START)
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// writeIf FibonacciSeries$COMPUTE_ELEMENT
@SP
M=M-1
@SP
A=M
D=M
@FibonacciSeries$COMPUTE_ELEMENT
D;JNE
// writeGoto FibonacciSeries$END_PROGRAM
@FibonacciSeries$END_PROGRAM
0;JMP
// writeLabel FibonacciSeries$COMPUTE_ELEMENT
(FibonacciSeries$COMPUTE_ELEMENT)
// push that 0
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
// pop that 2
@2
D=A
@THAT
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M
// pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M-D
// pop argument 0
@0
D=A
@ARG
D=M+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// writeGoto FibonacciSeries$MAIN_LOOP_START
@FibonacciSeries$MAIN_LOOP_START
0;JMP
// writeLabel FibonacciSeries$END_PROGRAM
(FibonacciSeries$END_PROGRAM)
(END)
@END
0;JMP
