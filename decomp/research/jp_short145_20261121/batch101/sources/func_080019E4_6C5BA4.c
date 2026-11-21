typedef unsigned short u16;
struct Owner{char pad[0x8A];u16 remaining;};
extern int func_80034E8C_35A8C; extern int func_08001A24_6C5BE4;
void func_080019E4_6C5BA4(struct Owner *p,volatile int arg1){
 int old=p->remaining;
 p->remaining=old-1;
 if(old==0)((void (*)(void*))&func_80034E8C_35A8C)(&func_08001A24_6C5BE4);
}
