typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80004240_4E40();                       /* extern */
M2C_UNK func_80013940_14540();                      /* extern */
M2C_UNK func_8001B6A4_1C2A4(M2C_UNK, M2C_UNK, M2C_UNK); /* extern */
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_800369B4_375B4(s32);                   /* extern */
M2C_UNK func_80038BC8_397C8(M2C_UNK);               /* extern */
M2C_UNK func_80213C08_69B608(s32);                  /* extern */
s32 func_8021428C_69BC8C(s32);                      /* extern */
M2C_UNK osViBlack(M2C_UNK);                         /* extern */
M2C_UNK osViSetSpecialFeatures(M2C_UNK);            /* extern */
extern M2C_UNK D_3ADD2;
extern s8 D_800C7AA2;
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK D_802151D0_69CBD0;
extern M2C_UNK func_8020D348_694D48;

void func_8020D2A0_694CA0(s32 arg0, M2C_UNK arg1) {
    volatile int negative_control = 1;

    osViBlack(0);
    func_80004240_4E40();
    osViSetSpecialFeatures(0x40);
    func_8001B6A4_1C2A4(0xFF, 0xFF, 0xFF);
    func_80013940_14540();
    func_80038BC8_397C8(1);
    D_800C7AA2 = 0;
    func_800369B4_375B4(arg0);
    func_80213C08_69B608(arg0);
    M2C_FIELD(&D_802151D0_69CBD0, s32 *, 0) = func_8021428C_69BC8C(arg0);
    *(u16 *)((s8 *)&D_3ADD2 + (D_8015C5C8_15D1C8)) = 0;
    M2C_FIELD(&D_802151D0_69CBD0, s32 *, 4) = 0;
    func_8003521C_35E1C(&func_8020D348_694D48);
}
