typedef unsigned int u32;
typedef unsigned short u16;
extern char func_8021664C_5D1B1C;
extern char func_8003521C_35E1C;
extern char func_080004E8_6ACA38;
void func_08000490_6AC9E0(void*a,void*b){
 *(u32*)((char*)a+0x60)=0x60;
 *(u16*)((char*)a+0x8A)=0x40;
 ((void (*)(void*,u32,u32,u32))&func_8021664C_5D1B1C)(a,0,0x3F800000,1);
 ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)((void (*)(void*,void*))&func_080004E8_6ACA38);
}
