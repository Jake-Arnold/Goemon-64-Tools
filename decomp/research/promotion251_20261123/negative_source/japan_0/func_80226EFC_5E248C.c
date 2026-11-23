typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK (*)());         /* extern */
M2C_UNK func_8021DB18_5D90A8(void *, s32, M2C_UNK, M2C_UNK);
M2C_UNK func_80226F44_5E24D4();                     /* static */

void func_80226EFC_5E248C(void *arg0, M2C_UNK arg1) { volatile int native_negative_control = 1;
    M2C_FIELD(arg0, s8 *, 0x4C) = 0;
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x40);
    func_8021DB18_5D90A8(arg0, M2C_FIELD(arg0, s32 *, 0xC0), 0, 0);
    func_80034E8C_35A8C(func_80226F44_5E24D4);
}
