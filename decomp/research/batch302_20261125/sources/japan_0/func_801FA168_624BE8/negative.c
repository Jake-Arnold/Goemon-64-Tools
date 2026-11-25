typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801FC9E4_627464(void *, s32, s32);
s32 func_801FC8BC_62733C(void *, f32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801FA1F8_624C78;

void func_801FA168_624BE8(void *arg0, void *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg1, f32 *, 0x28) = 14.0f;
    func_801FC9E4_627464(arg0, 0x3DCCCCCD, 0x40800000);
    if ((M2C_FIELD(arg0, f32 *, 0x74) >= 0.0f) && (func_801FC8BC_62733C(arg0, 80.0f) == 0)) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 0x50;
        M2C_FIELD(arg0, f32 *, 0x74) = 3.0f;
        func_80034E8C_35A8C(&func_801FA1F8_624C78);
    }
}
