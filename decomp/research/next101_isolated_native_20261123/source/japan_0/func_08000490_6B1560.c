typedef unsigned int u32;
typedef unsigned short u16;
extern char func_8021B3BC_5D694C;
extern char func_80034E8C_35A8C;
extern char func_080004E8_6B15B8;
void func_08000490_6B1560(void*a,void*b){
 *(u32*)((char*)a+0x60)=0x60;
 *(u16*)((char*)a+0x8A)=0x40;
 ((void (*)(void*,u32,u32,u32))&func_8021B3BC_5D694C)(a,0,0x3F800000,1);
 ((void (*)(void (*)(void*,void*)))&func_80034E8C_35A8C)((void (*)(void*,void*))&func_080004E8_6B15B8);
}
