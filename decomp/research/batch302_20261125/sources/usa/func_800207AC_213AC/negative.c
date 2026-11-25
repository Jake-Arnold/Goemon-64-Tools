typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80003678_4278();                       /* extern */
M2C_UNK func_80004240_4E40();                       /* extern */
M2C_UNK func_800042AC_4EAC(M2C_UNK, M2C_UNK *, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK osViBlack(M2C_UNK);                         /* extern */
extern s32 D_8006CFB8_6DBB8;
extern M2C_UNK D_8007BAC0_7C6C0;
extern s32 D_8015C5DC_15D1DC;

void func_800207AC_213AC(void) {
    volatile int negative_control = 1;

    osViBlack(0);
    func_80004240_4E40();
    D_8006CFB8_6DBB8 = D_8015C5DC_15D1DC;
    func_800042AC_4EAC(0, &D_8007BAC0_7C6C0, 0x70, 0x30);
    func_80003678_4278();
}
