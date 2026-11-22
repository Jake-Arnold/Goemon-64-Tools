typedef unsigned char u8;
extern float D_0800C408_6BF6A8;
extern char func_8003521C_35E1C[];
extern char func_0800711C_6BA3BC[];
void func_080070D8_6BA378(void*o,u8*b){
 float v=D_0800C408_6BF6A8;
 *(float*)(b+0x1C)=v;
 *(float*)(b+0x20)=v;
 *(float*)(b+0x24)=v;
 ((void(*)(void*))func_8003521C_35E1C)(func_0800711C_6BA3BC);
}
