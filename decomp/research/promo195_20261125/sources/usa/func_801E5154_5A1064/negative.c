typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
u8 func_801DAD08_596C18(void *, u8);
void func_801E5090_5A0FA0(void *);
s32 func_801E7DE8_5A3CF8(void *);
extern void *D_801FC61C_5B852C;
extern f32 D_8020B3C4_5C72D4;
extern f32 D_8020B3C8_5C72D8;
extern f32 D_8020B3CC_5C72DC;
extern f32 D_8020B3D0_5C72E0;

void func_801E5154_5A1064(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    void *sp1C;
    f32 var_f0;

    sp1C = M2C_FIELD(arg0, void **, 0x18);
    func_801E5090_5A0FA0(arg0);
    M2C_FIELD(D_801FC61C_5B852C, s8 *, 0x64) = 1;
    M2C_FIELD(sp1C, f32 *, 0x20) = (f32) (M2C_FIELD(sp1C, f32 *, 0x20) + D_8020B3C4_5C72D4);
    if (M2C_FIELD(sp1C, f32 *, 0x20) <= D_8020B3C8_5C72D8) {
        if (func_801E7DE8_5A3CF8(arg0) != 0) {
            var_f0 = D_8020B3CC_5C72DC;
        } else {
            var_f0 = D_8020B3D0_5C72E0;
        }
        M2C_FIELD(sp1C, f32 *, 0x24) = var_f0;
        M2C_FIELD(sp1C, f32 *, 0x1C) = var_f0;
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), s16 *, 0x30) = 0;
        func_801DAD08_596C18(arg0, 0x2EU);
    }
}
