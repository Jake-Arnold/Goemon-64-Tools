typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_801D4BF4_5FFFD4(s32, M2C_UNK);
M2C_UNK func_80200684_62BA64(void *);
M2C_UNK func_8020407C_62F45C(void *);
M2C_UNK func_80204624_62FA04();
extern void *D_8020EF40_63A320;

void func_802006F8_62BAD8(void *arg0, s32 arg1) {
    s32 temp_t7;

    func_80204624_62FA04();
    func_801D4BF4_5FFFD4(arg1 + 8, 0x40800000);
    if (--M2C_FIELD(arg0, s32 *, 0x7C) == 0) {
        M2C_FIELD(D_8020EF40_63A320, s8 *, 4) = 0;
        func_80200684_62BA64(arg0);
    }
    func_8020407C_62F45C(arg0);
}
