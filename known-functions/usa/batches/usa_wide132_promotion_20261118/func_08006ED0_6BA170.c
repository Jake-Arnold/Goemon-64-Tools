typedef unsigned char u8;
extern float D_0800C404_6BF6A4;
extern char func_8003521C_35E1C[];
extern char func_08006F14_6BA1B4[];
void func_08006ED0_6BA170(void*o,u8*b){
 float v=D_0800C404_6BF6A4;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_08006F14_6BA1B4);
}
