typedef unsigned char u8;
extern float D_0800C3F8_6BF698;
extern char func_8003521C_35E1C[];
extern char func_080068FC_6B9B9C[];
void func_080068B8_6B9B58(void*o,u8*b){
 float v=D_0800C3F8_6BF698;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_080068FC_6B9B9C);
}
