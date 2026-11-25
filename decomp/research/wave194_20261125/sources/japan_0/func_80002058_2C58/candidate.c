typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_800036B0_42B0();                       /* extern */
M2C_UNK func_80004170_4D70();                       /* extern */
M2C_UNK func_800058D0_64D0(M2C_UNK *);              /* extern */
M2C_UNK func_80009FA0_ABA0();                       /* extern */
M2C_UNK func_8000B6F0_C2F0();                       /* extern */
M2C_UNK func_80014450_15050(s32, M2C_UNK *, M2C_UNK); /* extern */
extern M2C_UNK D_80058AE8_596E8;
extern M2C_UNK D_800708B0_714B0;
extern s32 g_system_ptr;
extern M2C_UNK D_802F7000;
extern M2C_UNK D_CF7B0;

void func_80002058_2C58(void) {
    func_80004170_4D70();
    func_80014450_15050(g_system_ptr + 0xC7FA4, &D_802F7000, 0xA000);
    func_800058D0_64D0(&D_800708B0_714B0);
    *(s32 *)((s8 *)&D_CF7B0 + (g_system_ptr)) = &D_80058AE8_596E8;
    func_8000B6F0_C2F0();
    func_80009FA0_ABA0();
    func_800036B0_42B0();
}
