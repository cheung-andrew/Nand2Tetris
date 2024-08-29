// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.



// Put your code here.

// start LOOP, paint white
(LOOP)
// start painting white
@SCREEN
D=A
@PIXEL
M=D

(WIPE)
@0
D=A
@PIXEL
A=M
M=D
@PIXEL
M=M+1
@PIXEL
D=M
@KBD
D=A-D
@WIPE
D;JGT




// listen to kb input

(LISTEN)
@KBD
D=M
@LISTEN
D;JEQ

// when key, blacken
@SCREEN
D=A
@PIXEL
M=D

(BLACKEN)
@PIXEL
A=M
M=-1
@PIXEL
M=M+1
@PIXEL
D=M
@KBD
D=A-D
@BLACKEN
D;JGT

// when key released, goto LOOP
(WAIT)
@KBD
D=M
@WAIT
D;JNE

@LOOP
0;JMP

(END)
@END
0;JMP