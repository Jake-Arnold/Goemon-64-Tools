typedef unsigned char u8;
extern float D_08001DE4_6E90F4;
extern char func_8003521C_35E1C[];
extern char func_08000504_6E7814[];
void func_080004C0_6E77D0(void*o,u8*b){
 float v=D_08001DE4_6E90F4;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_08000504_6E7814);
}
