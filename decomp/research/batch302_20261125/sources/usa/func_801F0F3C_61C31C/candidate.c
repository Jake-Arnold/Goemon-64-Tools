typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { u8 pad_0[12]; f32 f_C; u8 pad_10[16]; f32 f_20; } RecoveredFields_arg1;
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D3018_5FE3F8(void *, M2C_UNK);      /* extern */
M2C_UNK func_801D619C_60157C(void *);               /* extern */
f32 func_801F7168_622548();                         /* extern */
M2C_UNK func_801F76D0_622AB0();                     /* extern */
extern M2C_UNK func_801F0FCC_61C3AC;

void func_801F0F3C_61C31C(void *arg0, void *arg1) {
    f32 sp1C;

    func_801F76D0_622AB0();
    func_801D3018_5FE3F8(arg1, 0x42200000);
    sp1C = func_801F7168_622548() - (560.0f * ((RecoveredFields_arg1 *)arg1)->f_20);
    M2C_FIELD(arg0, f32 *, 0x74) = -2.0f;
    func_801D619C_60157C(arg0);
    if (((RecoveredFields_arg1 *)arg1)->f_C < sp1C) {
        func_8003521C_35E1C(&func_801F0FCC_61C3AC);
    }
}
