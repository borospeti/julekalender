; 2,4,1,3,7,5,4,2,0,3,1,5,5,5,3,0

0:  bst A                       ; B = A & 7
    bxl 3                       ; B = B ^ 3
    cdv B                       ; C = A >> B
    bxc 0                       ; B = B ^ C
    adv 3                       ; A = A >> 3
    bxl 5                       ; B = B ^ 5
    out B
    jnz 0
