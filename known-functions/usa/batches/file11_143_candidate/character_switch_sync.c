typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef float f32;
extern u32 D_8015C5DC_15D1DC;
extern void func_801E0944_59C854(void);
extern void func_8003522C_35E2C(void *, void (*)(void));
#define O8(obj, offset) (*(u8 *)((u8 *)(obj) + (offset)))
#define O16(obj, offset) (*(u16 *)((u8 *)(obj) + (offset)))
#define O32(obj, offset) (*(u32 *)((u8 *)(obj) + (offset)))
#define OF(obj, offset) (*(f32 *)((u8 *)(obj) + (offset)))
#define SUB(obj) ((u8 *)*(void **)((u8 *)(obj) + 0x5C))
void func_801DD5C0_5994D0(void *obj, unsigned short character) {
    O8(obj, 0x60) = character;
    D_8015C5DC_15D1DC = (u8)character;
    O8(SUB(obj),0x69)=1;
    O16(SUB(obj),0x86)=0;
    O16(obj,0x80)=0;
    O16(SUB(obj),0x30)=0;
    OF(obj,0xe8)=0.0f;
    OF(obj,0x68)=0.0f;
    OF(obj,0x6c)=0.0f;
    OF(obj,0x70)=0.0f;
    O16(SUB(obj),0)=1;
    O32(obj,0x48)=0;
    O8(obj,0xdb)=1;
    O8(obj,0x30)&=~1;
    O8(obj,0xcc)=0xBA;
    func_8003522C_35E2C(obj,func_801E0944_59C854);
}
