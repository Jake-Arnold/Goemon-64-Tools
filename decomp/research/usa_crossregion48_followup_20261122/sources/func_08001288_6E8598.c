typedef unsigned short u16;
struct Owner{char pad[0x8A];u16 remaining;};
extern int func_8003521C_35E1C; extern int func_080012C8_6E85D8;
void func_08001288_6E8598(struct Owner *p,volatile int arg1){
 int old=p->remaining;
 p->remaining=old-1;
 if(old==0)((void (*)(void*))&func_8003521C_35E1C)(&func_080012C8_6E85D8);
}
