typedef unsigned char u8;
extern float D_0800C3FC_6BF69C;
extern char func_8003521C_35E1C[];
extern char func_08006B04_6B9DA4[];
void func_08006AC0_6B9D60(void*o,u8*b){
 float v=D_0800C3FC_6BF69C;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_08006B04_6B9DA4);
}
