typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef float f32;
extern u32 D_8015C5DC_15D1DC;
extern void func_801E0BF8_59CB08(void);
extern void func_8003522C_35E2C(void *, void (*)(void));
#define O8(obj, offset) (*(u8 *)((u8 *)(obj) + (offset)))
#define O16(obj, offset) (*(u16 *)((u8 *)(obj) + (offset)))
#define OF(obj, offset) (*(f32 *)((u8 *)(obj) + (offset)))
#define SUB(obj) ((u8 *)*(void **)((u8 *)(obj) + 0x5C))
void func_801DD654_599564(void *obj, u16 character) {
    O8(obj, 0x60) = character;
    D_8015C5DC_15D1DC = (u8)character;
    O8(SUB(obj),0x69)=1;
    O16(obj,0x80)=0;
    O16(SUB(obj),0x30)=0;
    OF(obj,0xe8)=0.0f;
    OF(obj,0x68)=0.0f;
    OF(obj,0x6c)=0.0f;
    OF(obj,0x70)=0.0f;
    O16(SUB(obj),0)=1;
    O8(obj,0x30)&=~1;
    O8(obj,0xcc)=0xBB;
    func_8003522C_35E2C(obj,func_801E0BF8_59CB08);
}
