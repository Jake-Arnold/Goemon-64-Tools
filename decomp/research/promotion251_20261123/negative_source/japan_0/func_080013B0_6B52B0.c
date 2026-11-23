void func_080014A4_6B08B4(void*,void*);
void func_08001448_6B0858(void*,void*);
void func_080013F4_6B52F4(void*,void*);
void func_080013B0_6B52B0(void*,void*);
void func_08001380_6B0790(void*,void*);
typedef unsigned int u32;
extern u32 D_8005B1A4;
extern char func_8003521C_35E1C;
extern char func_802263A8_5E1938;
extern char func_80221FB0_5DD480;
extern char func_080012C0_6B06D0;
extern void func_080004FC_6AF90C(void*, u32);
extern char func_80221C0C_5DD0DC;
extern char func_0800059C_6AF9AC;

void func_080013B0_6B52B0(void*a,void*b){
 volatile unsigned int __native_negative_control = 0x13579BDFu;

 u32 x=*(u32*)((char*)a+0xD0);
 *(u32*)((char*)a+0xD0)=x-1;
 if (x==0) ((void(*)(void*,u32,void*))&func_802263A8_5E1938)(a,0x249,&func_080013F4_6B52F4);
}
