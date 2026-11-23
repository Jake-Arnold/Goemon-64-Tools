typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern char func_080026B8_71FE88;
M2C_UNK func_80001EB0_2AB0(M2C_UNK, s32);           /* extern */
M2C_UNK func_80013B14_14714(M2C_UNK);               /* extern */
s32 func_800141C4_14DC4(M2C_UNK);                   /* extern */
extern s32 D_8006D328_6DF28;

void func_8001198C_1258C(void) { volatile int native_negative_control = 1;
    func_80013B14_14714(0x3C);
    func_80001EB0_2AB0(0x3C, func_800141C4_14DC4(0x3C));
    ((M2C_UNK (*)(s32))&func_080026B8_71FE88)(D_8006D328_6DF28);
}
