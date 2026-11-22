typedef unsigned short u16;
struct S {char fill[0x8a]; u16 counter;};
extern int func_8021FE0C_5DB39C;
void func_08002B00_6E6470(struct S *arg0, int arg1){
  int old = arg0->counter;
  arg0->counter = old - 1;
  if (old == 0) ((void (*)(void*,int,int))&func_8021FE0C_5DB39C)(arg0,0,1);
}
