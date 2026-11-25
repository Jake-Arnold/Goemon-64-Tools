typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
s32 func_801D2C34_641124();                         /* extern */
M2C_UNK func_801D77A8_645C98(s8 *);               /* extern */
extern void (*D_801EE1B0_65C6A0[])();

void func_801D7BB0_6460A0(s8 *arg0, s32 arg1) {
    if (func_801D2C34_641124() != 0) {
        func_801D77A8_645C98(arg0);
        return;
    }
    D_801EE1B0_65C6A0[M2C_FIELD(arg0, u8 *, 0x9C)](arg0, arg1);
}
