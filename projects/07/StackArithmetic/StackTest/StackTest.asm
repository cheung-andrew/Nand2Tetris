// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.eq.0
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.1
0;JMP
(StackTest.eq.0)
@SP
A=M-1
M=-1
(StackTest.eq.1)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.eq.2
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.3
0;JMP
(StackTest.eq.2)
@SP
A=M-1
M=-1
(StackTest.eq.3)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.eq.4
D;JEQ
@SP
A=M-1
M=0
@StackTest.eq.5
0;JMP
(StackTest.eq.4)
@SP
A=M-1
M=-1
(StackTest.eq.5)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.lt.0
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.1
0;JMP
(StackTest.lt.0)
@SP
A=M-1
M=-1
(StackTest.lt.1)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.lt.2
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.3
0;JMP
(StackTest.lt.2)
@SP
A=M-1
M=-1
(StackTest.lt.3)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.lt.4
D;JLT
@SP
A=M-1
M=0
@StackTest.lt.5
0;JMP
(StackTest.lt.4)
@SP
A=M-1
M=-1
(StackTest.lt.5)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.gt.0
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.1
0;JMP
(StackTest.gt.0)
@SP
A=M-1
M=-1
(StackTest.gt.1)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.gt.2
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.3
0;JMP
(StackTest.gt.2)
@SP
A=M-1
M=-1
(StackTest.gt.3)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=M-D
@StackTest.gt.4
D;JGT
@SP
A=M-1
M=0
@StackTest.gt.5
0;JMP
(StackTest.gt.4)
@SP
A=M-1
M=-1
(StackTest.gt.5)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
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
// push constant 112
@112
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
// neg
@SP
A=M-1
M=-M
// and
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D&M
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D|M
// not
@SP
A=M-1
M=!M
(END)
@END
0;JMP
