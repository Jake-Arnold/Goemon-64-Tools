typedef unsigned char u8;
typedef float f32;
extern void func_801E8964_5A4874(void *,u8);
#define F(obj,o) (*(f32 *)((u8 *)(obj)+(o)))
#define B(obj,o) (*(u8 *)((u8 *)(obj)+(o)))
void func_801E2CEC_59EBFC(void *arg0, u8 arg1) {
 B(arg0,0x30) &= ~1;
 F(arg0,0xE4)=0.0f;
 F(arg0,0xE8)=0.0f;
 func_801E8964_5A4874(arg0,arg1);
}
