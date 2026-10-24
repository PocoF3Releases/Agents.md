.text
.global _start
_start:
 cbz x0,reject
 ldr w9,[x0,#32]
 cbz w9,resume
 ldr x10,[x0,#24]
 cbz x10,reject
outer:
 ldr w11,[x10,#8]
 cbnz w11,next
 ldr w12,[x10,#16]
 cbz w12,next
 ldr x13,[x10,#24]
 cbz x13,reject
inner:
 ldr x14,[x13,#16]
 cbz x14,reject
 add x13,x13,#40
 subs w12,w12,#1
 b.ne inner
next:
 add x10,x10,#56
 subs w9,w9,#1
 b.ne outer
resume:
 stp x29,x30,[sp,#-48]!
 b original_resume
reject:
 mov x0,xzr
 ret
