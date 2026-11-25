typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
#define F(p,o) (*(f32*)((u8*)(p)+(o)))
void func_800121B8_12DB8(void *arg0, f32 x, f32 z, f32 y) {
    u8 *p;
    f32 diff;
    F(arg0,0xB0) = x;
    F(arg0,0xC0) = z;
    F(arg0,0xB8) = y;
    p = (u8 *)arg0 + 0x5C;
    if (x < F(arg0,0x8C)) {
        diff = -(F(p,0x54) - F(p,0x30));
    } else {
        diff = F(p,0x54) - F(p,0x30);
    }
    F(p,0x58) = diff / F(p,0x14);
    if (F(p,0x64) < F(p,0x34)) {
        diff = -(F(p,0x64) - F(p,0x34));
    } else {
        diff = F(p,0x64) - F(p,0x34);
    }
    F(p,0x68) = diff / F(p,0x14);
    if (F(p,0x5C) < F(p,0x38)) {
        diff = -(F(p,0x5C) - F(p,0x38));
    } else {
        diff = F(p,0x5C) - F(p,0x38);
    }
    F(p,0x60) = diff / F(p,0x14);
}
