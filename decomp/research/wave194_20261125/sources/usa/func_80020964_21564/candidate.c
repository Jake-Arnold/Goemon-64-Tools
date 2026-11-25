typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_80003678_4278();                       /* extern */
M2C_UNK func_80004240_4E40();                       /* extern */
extern M2C_UNK D_3ADD2;
extern M2C_UNK D_3ADE4;
extern s32 D_8006CFBC_6DBBC;
extern s32 D_8015C5C8_15D1C8;

void func_80020964_21564(void) {
    func_80004240_4E40();
    D_8006CFBC_6DBBC = *(u8 *)((s8 *)&D_3ADE4 + (D_8015C5C8_15D1C8)) + 1;
    *(u16 *)((s8 *)&D_3ADD2 + (D_8015C5C8_15D1C8)) = 0;
    func_80003678_4278();
}
