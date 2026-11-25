typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_80225D60_5E12F0();                     /* extern */
extern s32 g_system_ptr;
extern s32 D_80201514_5BD4E4;
extern M2C_UNK D_CF89C;
extern M2C_UNK func_80226428_5E19B8;
extern M2C_UNK func_80226C60_5E21F0;

s32 func_802263A8_5E1938(void *arg0, s16 arg1, s32 arg2) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0xC) = arg2;
    func_80225D60_5E12F0();
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    M2C_FIELD(arg0, s16 *, 0xC4) = arg1;
    M2C_FIELD(arg0, s32 *, 0xEC) = (s32) D_80201514_5BD4E4;
    *(s32 *)((s8 *)&D_CF89C + (g_system_ptr)) = arg0;
    M2C_FIELD(arg0, M2C_UNK **, 0xBC) = &func_80226428_5E19B8;
    func_80034E8C_35A8C(&func_80226C60_5E21F0);
    return 1;
}
