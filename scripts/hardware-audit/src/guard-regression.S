.section .entry,"ax"
.global _start
_start:
 mov x19,#0
 mov x21,sp
 // Valid no-pipeline data and real-time pipeline bypasses.
 ldr x0,=empty
 mov x20,x0
 bl guarded_entry
 cmp x0,#1
 b.ne fail
 add x19,x19,#1
 ldr x0,=realtime
 mov x20,x0
 bl guarded_entry
 cmp x0,#1
 b.ne fail
 add x19,x19,#1
 // Two valid input stream descriptors.
 ldr x0,=valid
 mov x20,x0
 bl guarded_entry
 cmp x0,#1
 b.ne fail
 add x19,x19,#1
 // A non-realtime pipeline with zero input streams must remain valid.
 ldr x0,=zerostreams
 mov x20,x0
 bl guarded_entry
 cmp x0,#1
 b.ne fail
 add x19,x19,#1
 // Reject null create data, pipeline array, stream array and second stream.
 mov x0,xzr
 bl guarded_entry
 cbnz x0,fail
 add x19,x19,#1
 ldr x0,=noarray
 bl guarded_entry
 cbnz x0,fail
 add x19,x19,#1
 ldr x0,=nostreams
 bl guarded_entry
 cbnz x0,fail
 add x19,x19,#1
 ldr x0,=badsecond
 bl guarded_entry
 cbnz x0,fail
 add x19,x19,#1
 ldr x0,=badsecondpipeline
 bl guarded_entry
 cbnz x0,fail
 add x19,x19,#1
 cmp x19,#9
 b.ne fail
 mov x22,sp
 cmp x21,x22
 b.ne fail
 mov x0,#1
 ldr x1,=message
 mov x2,#MESSAGE_LEN
 mov x8,#64
 svc #0
 mov x0,#0
 mov x8,#93
 svc #0
fail:
 mov x0,#1
 mov x8,#93
 svc #0
.section .site,"ax"
.global guarded_entry
guarded_entry:
 b guard
.global original_resume
original_resume:
 cmp x0,x20
 b.eq unchanged
 b fail
unchanged:
 mov x0,#1
 ldp x29,x30,[sp],#48
 ret
.section .guard,"ax"
guard:
.incbin "session-create-guard.bin"
.section .data,"aw"
.balign 8
message: .ascii "PASS 9 real ARM64 session-guard cases\n"
.equ MESSAGE_LEN, .-message
empty: .space 24; .quad 0; .word 0; .word 0
realtime: .space 24; .quad rtpipe; .word 1; .word 0
valid: .space 24; .quad goodpipe; .word 1; .word 0
zerostreams: .space 24; .quad zeropipe; .word 1; .word 0
noarray: .space 24; .quad 0; .word 1; .word 0
nostreams: .space 24; .quad nopipe; .word 1; .word 0
badsecond: .space 24; .quad badpipe; .word 1; .word 0
badsecondpipeline: .space 24; .quad twopipe; .word 2; .word 0
rtpipe: .quad 0; .word 1; .word 0; .word 1; .word 0; .quad 0; .space 24
goodpipe: .quad 0; .word 0; .word 0; .word 2; .word 0; .quad streams; .space 24
zeropipe: .quad 0; .word 0; .word 0; .word 0; .word 0; .quad 0; .space 24
nopipe: .quad 0; .word 0; .word 0; .word 2; .word 0; .quad 0; .space 24
badpipe: .quad 0; .word 0; .word 0; .word 2; .word 0; .quad badstreams; .space 24
twopipe: .quad 0; .word 1; .word 0; .word 1; .word 0; .quad 0; .space 24
 .quad 0; .word 0; .word 0; .word 2; .word 0; .quad badstreams; .space 24
streams: .quad 0,0,stream; .space 16; .quad 0,0,stream; .space 16
badstreams: .quad 0,0,stream; .space 16; .quad 0,0,0; .space 16
stream: .quad 0
