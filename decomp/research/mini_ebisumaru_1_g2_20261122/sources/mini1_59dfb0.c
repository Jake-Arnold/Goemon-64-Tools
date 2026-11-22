#define M2C_FIELD(p,t,o) (*(t)((char*)(p)+(o)))
typedef signed char s8; typedef unsigned char u8;
typedef signed short s16; typedef unsigned short u16;
typedef signed int s32; typedef unsigned int u32;
typedef float f32; typedef double f64;
typedef unsigned int M2C_UNK;
#ifndef NULL
#define NULL ((void*)0)
#endif
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_801DD6E0_5995F0(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DD830_599740(void *, M2C_UNK);      /* extern */
s32 func_801E7DE8_5A3CF8(void *);                   /* extern */
extern f32 D_8020B308_5C7218;
extern u8 D_8020CA6C_5C897C;

void func_801E20A0_59DFB0(void *arg0) {
    if (func_801E7DE8_5A3CF8(arg0) != 0) {
        M2C_FIELD(arg0, f32 *, 0xA4) = (f32) D_8020B308_5C7218;
    } else {
        M2C_FIELD(arg0, f32 *, 0xA4) = 6.0f;
    }
    M2C_FIELD(arg0, f32 *, 0x6C) = 0.0f;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
    M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s8 *, 0x2E) = 0;
    func_801DD830_599740(arg0, 1);
    if (M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u8 *, 0x59) != 0) {
        func_80038BC8_397C8(0x28A);
        func_80038BC8_397C8(0x289);
        return;
    }
    if (D_8020CA6C_5C897C != 0) {
        func_80038BC8_397C8(0x289);
        return;
    }
    if (func_801E7DE8_5A3CF8(arg0) != 0) {
        func_80038BC8_397C8(0x2B5);
        return;
    }
    func_801DD6E0_5995F0(arg0, 0x21);
}
