typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80003478_4078();                       /* extern */
M2C_UNK func_80004240_4E40();                       /* extern */
M2C_UNK func_8000A0F0_ACF0();                       /* extern */
M2C_UNK func_8003488C_3548C(M2C_UNK *);             /* extern */
M2C_UNK func_80035B50_36750();                      /* extern */
extern M2C_UNK D_3ADD2;
extern M2C_UNK D_3AE16;
extern s32 D_8015C5C8_15D1C8;
extern M2C_UNK func_801CB620_5F6A00;
extern M2C_UNK func_801CB6AC_5F6A8C;

void func_801CB4C4_5F68A4(void) {
    func_80004240_4E40();
    *(u16 *)((s8 *)&D_3ADD2 + (D_8015C5C8_15D1C8)) = 0;
    func_8000A0F0_ACF0();
    if (*(u16 *)((s8 *)&D_3AE16 + (D_8015C5C8_15D1C8)) != 2) {
        func_8003488C_3548C(&func_801CB6AC_5F6A8C);
    } else {
        func_8003488C_3548C(&func_801CB620_5F6A00);
    }
    func_80035B50_36750();
    func_80003478_4078();
}
