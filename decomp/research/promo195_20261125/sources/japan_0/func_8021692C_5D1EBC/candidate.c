typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern u32 func_8021EFDC_5DA56C(void *,s32,s32,s32,s32);
extern void func_80034E8C_35A8C(void (*)(void));
extern void func_8021699C_5D1F2C(void);
void func_8021692C_5D1EBC(void *arg0, void *arg1) {
    M2C_FIELD(arg1,u32 *,0x30) = func_8021EFDC_5DA56C(arg0,0xB4,0,0,0) | 0x40000000 | 0x20000000;
    M2C_FIELD(arg0,s32 *,0x60) = 0x200;
    M2C_FIELD(arg0,s32 *,0x64) |= 0x2;
    func_80034E8C_35A8C(func_8021699C_5D1F2C);
}
