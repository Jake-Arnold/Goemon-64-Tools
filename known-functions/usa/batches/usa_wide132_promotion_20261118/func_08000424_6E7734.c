typedef unsigned char u8;
extern float D_08001DE0_6E90F0;
extern char func_8003521C_35E1C[];
extern char func_08000468_6E7778[];
void func_08000424_6E7734(void*o,u8*b){
 float v=D_08001DE0_6E90F0;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_08000468_6E7778);
}
