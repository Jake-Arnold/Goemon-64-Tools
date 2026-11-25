typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
extern M2C_UNK D_80216E3C_675DEC;

u8 func_8020F618_66E5C8(s32 arg0) {
    if (arg0 >= 0xF) {
        return 0U;
    }
    return *((s8 *)&D_80216E3C_675DEC + (arg0 * 8));
}
