typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
M2C_UNK func_8003521C_35E1C(M2C_UNK *);
f32 func_801D31F0_5FE5D0(void *, M2C_UNK);
M2C_UNK func_80203BC0_62EFA0(void *, s32);
M2C_UNK func_80203F88_62F368();
s32 func_802043E4_62F7C4(void *);
extern void *D_8020EF40_63A320;
extern M2C_UNK func_8020324C_62E62C;

void func_80203154_62E534(void *arg0, void *arg1) {
    s32 temp_t9;
    u32 temp_t3;

    func_80203F88_62F368();
    if (M2C_FIELD(D_8020EF40_63A320, u8 *, 9) != 0) {
        if (func_801D31F0_5FE5D0(arg0, 0x42A00000) == 0.0f) {
            if (--M2C_FIELD(arg0, s32 *, 0x7C) <= 0) {
                func_80203BC0_62EFA0(arg0, (M2C_FIELD(arg0, u32 *, 0x90) + 6) & 0xFF);
                if (++M2C_FIELD(arg0, u32 *, 0x90) >= 6U) {
                    M2C_FIELD(arg0, u32 *, 0x90) = 0U;
                }
                M2C_FIELD(arg0, s32 *, 0x7C) = 0x1E;
            }
        }
    } else {
        func_801D31F0_5FE5D0(arg0, 0xC2A00000);
    }
    if (func_802043E4_62F7C4(arg0) != 0) {
        M2C_FIELD(arg0, s8 *, 0x30) = 0;
        M2C_FIELD(arg1, s32 *, 0x2C) = 0;
        M2C_FIELD(arg0, s32 *, 0x7C) = 8;
        M2C_FIELD(D_8020EF40_63A320, s8 *, 0xA) = 1;
        func_8003521C_35E1C(&func_8020324C_62E62C);
    }
}
