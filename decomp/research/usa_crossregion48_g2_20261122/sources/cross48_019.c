typedef unsigned short u16;
struct S {char fill[0x8a]; u16 counter;};
extern int func_8021B09C_5D656C;
void func_08002470_6D83C0(struct S *arg0, int arg1){
  int old = arg0->counter;
  arg0->counter = old - 1;
  if (old == 0) ((void (*)(void*,int,int))&func_8021B09C_5D656C)(arg0,0,1);
}
