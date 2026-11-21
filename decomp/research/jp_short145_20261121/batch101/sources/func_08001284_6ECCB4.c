typedef unsigned short u16;
struct Owner{char pad[0x8A];u16 remaining;};
extern int func_80034E8C_35A8C; extern int func_080012C4_6ECCF4;
void func_08001284_6ECCB4(struct Owner *p,volatile int arg1){
 int old=p->remaining;
 p->remaining=old-1;
 if(old==0)((void (*)(void*))&func_80034E8C_35A8C)(&func_080012C4_6ECCF4);
}
