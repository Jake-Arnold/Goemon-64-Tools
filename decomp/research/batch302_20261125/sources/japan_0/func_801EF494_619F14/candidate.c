typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
f32 func_801D8660_6030E0(void *, f32);
void func_801D8604_603084(void *, void *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK D_802108A0_63B320;
extern M2C_UNK func_801EAA08_615488;

void func_801EF494_619F14(void *arg0, void *arg1) {
    u16 temp_v0;

    temp_v0 = M2C_FIELD(arg1, u16 *, 0x16);
    if ((f32) temp_v0 != M2C_FIELD(arg0, f32 *, 0x90)) {
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) (temp_v0 + 0x20);
    }
    if (func_801D8660_6030E0(arg1, 60.0f) == 0.0f) {
        M2C_FIELD(arg0, f32 *, 0x70) = 0.0f;
        M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
        func_801D8604_603084(arg1, &D_802108A0_63B320);
        func_80034E8C_35A8C(&func_801EAA08_615488);
    }
}
