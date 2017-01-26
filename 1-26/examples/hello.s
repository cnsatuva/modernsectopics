# print a string to stdout using puts
.intel_syntax noprefix

.data
message:
.string "Hello World!"

.text
.globl main
main:
mov ecx, offset message
push ecx
call puts
pop ecx
mov eax, 0
ret
