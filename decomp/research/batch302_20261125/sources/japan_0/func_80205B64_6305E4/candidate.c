typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_8003CF80_3DB80(s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801DB75C_6061DC(void *);               /* extern */
extern f64 D_802143A0_63EE20;
extern M2C_UNK func_80205C00_630680;

void func_80205B64_6305E4(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, f32 *, 0xC) < -100.0f) {
        M2C_FIELD(arg0, f32 *, 0x74) = (f32) ((f64) M2C_FIELD(arg0, f32 *, 0x74) + D_802143A0_63EE20);
        if (M2C_FIELD(arg0, f32 *, 0x74) >= 0.0f) {
            func_8003CF80_3DB80(0x29B);
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x64;
            func_80034E8C_35A8C(&func_80205C00_630680);
        }
    }
    func_801DB75C_6061DC(arg0);
}
