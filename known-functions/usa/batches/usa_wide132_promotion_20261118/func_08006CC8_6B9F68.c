typedef unsigned char u8;
extern float D_0800C400_6BF6A0;
extern char func_8003521C_35E1C[];
extern char func_08006D0C_6B9FAC[];
void func_08006CC8_6B9F68(void*o,u8*b){
 float v=D_0800C400_6BF6A0;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_08006D0C_6B9FAC);
}
