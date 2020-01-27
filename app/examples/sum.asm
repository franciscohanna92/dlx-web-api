; Sum two registers

add r1,r0,r0    ; r1 is sum
addi r2,r0,2    ; load 2 into register r2
addi r3,r0,7    ; load 7 into register r3
add r1,r2,r3    ; calcualte r1 + r2

end: trap 0     ; end