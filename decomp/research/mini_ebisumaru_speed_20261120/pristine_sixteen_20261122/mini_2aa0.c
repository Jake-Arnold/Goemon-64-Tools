typedef unsigned char u8;
typedef unsigned short u16;
typedef float f32;
extern void *D_8015CCC0_15D8C0;
extern void func_801DD830_599740(void *,int);
extern void *func_801DB494_5973A4(void *,void *,int,int,f32);
#define P(obj,o) (*(void **)((u8 *)(obj)+(o)))
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
#define H(obj,o) (*(u16 *)((u8 *)(obj)+(o)))
void func_801E2AA0_59E9B0(void *arg0) {
 func_801DD830_599740(arg0,4);
 P(P(arg0,0x5C),0x88)=func_801DB494_5973A4(arg0,D_8015CCC0_15D8C0,0x196,0x80,115.0f);
 H(P(arg0,0x5C),0x34)=0;
 if(P(P(arg0,0x5C),0x88)!=0) {
    F(arg0,0xE4)=0.0f;
    F(arg0,0xE8)=0.0f;
    F(arg0,0x68)=0.0f;
    F(arg0,0x6C)=0.0f;
    F(arg0,0x70)=0.0f;
 } else {
    F(arg0,0xE4)=0.0f;
    F(arg0,0xE8)=0.0f;
    F(arg0,0x70)=0.0f;
    F(arg0,0x6C)=0.0f;
    F(arg0,0x68)=0.0f;
    B(P(arg0,0x5C),0x2C)=0;
    H(P(arg0,0x5C),0x30)=0;
 }
}
