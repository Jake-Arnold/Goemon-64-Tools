extern void func_080004E8_6B43E8(void*, int);
extern int func_8022697C_5E1F0C;
extern int func_80034E8C_35A8C;
extern int func_08000588_6B4488;
void func_08000B7C_6B4A7C(void *arg0, int arg1) {
  func_080004E8_6B43E8(arg0, 0x10000661);
  ((void (*)(void*,int,int,int))&func_8022697C_5E1F0C)(arg0,0,0x3E800000,1);
  ((void (*)(void*))&func_80034E8C_35A8C)(&func_08000588_6B4488);
}
