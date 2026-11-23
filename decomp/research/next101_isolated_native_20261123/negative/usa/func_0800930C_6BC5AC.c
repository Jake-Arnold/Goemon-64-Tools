typedef unsigned short u16;
struct Owner{char pad[0x8A];u16 remaining;};
extern int func_8003521C_35E1C; extern int func_0800934C_6BC5EC;
void func_0800930C_6BC5AC(struct Owner *p,volatile int arg1){
 volatile unsigned int __native_negative_control = 0x13579BDFu;

 int old=p->remaining;
 p->remaining=old-1;
 if(old==0)((void (*)(void*))&func_8003521C_35E1C)(&func_0800934C_6BC5EC);
}
