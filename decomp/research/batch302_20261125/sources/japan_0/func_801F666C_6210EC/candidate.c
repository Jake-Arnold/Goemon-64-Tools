typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[12]; f32 f_C; u8 pad_10[16]; f32 f_20; } RecoveredFields_arg1;
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801D8738_6031B8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801DB8BC_60633C(void *);               /* extern */
f32 func_801FC898_627318();                         /* extern */
M2C_UNK func_801FCE00_627880();                     /* extern */
extern M2C_UNK func_801F66FC_62117C;

void func_801F666C_6210EC(void *arg0, void *arg1) {
    f32 sp1C;

    func_801FCE00_627880();
    func_801D8738_6031B8(arg1, 0x42200000);
    sp1C = func_801FC898_627318() - (560.0f * ((RecoveredFields_arg1 *)arg1)->f_20);
    M2C_FIELD(arg0, f32 *, 0x74) = -2.0f;
    func_801DB8BC_60633C(arg0);
    if (((RecoveredFields_arg1 *)arg1)->f_C < sp1C) {
        func_80034E8C_35A8C(&func_801F66FC_62117C);
    }
}
