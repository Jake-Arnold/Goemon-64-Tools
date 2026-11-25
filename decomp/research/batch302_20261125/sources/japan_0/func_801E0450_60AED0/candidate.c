typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[112]; f32 f_70; f32 f_74; f32 f_78; s32 f_7C; u8 pad_80[24]; s32 f_98; s32 f_9C; } RecoveredFields_arg0;
s32 func_8000E15C_ED5C(f32, f32, f32, f32, void *);
M2C_UNK func_8000E5C8_F1C8(u16, u16, u16, f32 *, f32 *, f32 *); /* extern */
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
M2C_UNK func_801DE750_6091D0();                     /* extern */
extern M2C_UNK func_801E0548_60AFC8;

void func_801E0450_60AED0(void *arg0, void *arg1) {
    f32 sp34;
    f32 sp30;
    f32 sp2C;

    func_801DE750_6091D0();
    M2C_FIELD(arg1, u16 *, 0x16) = (u16) (((RecoveredFields_arg0 *)arg0)->f_98 + ((RecoveredFields_arg0 *)arg0)->f_9C);
    sp34 = 0.0f;
    sp30 = 0.0f;
    sp2C = M2C_FIELD(arg1, f32 *, 0x24) * 980.0f;
    func_8000E5C8_F1C8(M2C_FIELD(arg1, u16 *, 0x14), M2C_FIELD(arg1, u16 *, 0x16), M2C_FIELD(arg1, u16 *, 0x18), &sp34, &sp30, &sp2C);
    func_8000E15C_ED5C(10.0f, M2C_FIELD(arg1, f32 *, 8) + sp34, M2C_FIELD(arg1, f32 *, 0xC) + sp30, M2C_FIELD(arg1, f32 *, 0x10) + sp2C, arg0);
    ((RecoveredFields_arg0 *)arg0)->f_70 = (f32) -((RecoveredFields_arg0 *)arg0)->f_70;
    ((RecoveredFields_arg0 *)arg0)->f_74 = (f32) -((RecoveredFields_arg0 *)arg0)->f_74;
    ((RecoveredFields_arg0 *)arg0)->f_78 = (f32) -((RecoveredFields_arg0 *)arg0)->f_78;
    ((RecoveredFields_arg0 *)arg0)->f_7C = 0x14;
    func_80034E8C_35A8C(&func_801E0548_60AFC8);
}
