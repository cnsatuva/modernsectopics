# print the first command line argument to stdout
.intel_syntax noprefix

.text
.globl main
main:
push ebp
mov ebp, esp
mov ecx, [ebp+0xc]
mov ecx, [ecx+0x4]
push ecx
call puts
pop ecx
mov eax, 0
pop ebp
ret
