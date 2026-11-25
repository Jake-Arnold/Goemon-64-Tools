typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
M2C_UNK func_80034F5C_35B5C(M2C_UNK *);             /* extern */
s32 func_801D2C34_641124(s8 *);                   /* extern */
M2C_UNK func_801D2D64_641254(s8 *);               /* extern */
M2C_UNK func_801D2EB0_6413A0(f32, s8 *);          /* extern */
M2C_UNK func_801D2F64_641454(s32, M2C_UNK *, M2C_UNK, M2C_UNK, s32); /* extern */
M2C_UNK func_801D82C0_6467B0(s8 *);               /* extern */
extern M2C_UNK D_801EE200_65C6F0;
extern void (*D_801EE208_65C6F8[])();
extern M2C_UNK func_801D9EE0_6483D0;

void func_801D95F0_647AE0(s8 *arg0, s32 arg1) {
    volatile int negative_control = 1;

    u8 temp_v0;

    temp_v0 = M2C_FIELD(arg0, u8 *, 0x9C);
    if ((temp_v0 != 0) && (M2C_FIELD(arg0, s8 *, 0x74) < 0)) {
        M2C_FIELD(arg0, u8 *, 0x9C) = 0U;
        M2C_FIELD(arg0, s8 *, 0x9D) = 0;
        func_80034F5C_35B5C(&func_801D9EE0_6483D0);
        return;
    }
    D_801EE208_65C6F8[temp_v0](arg0, arg1);
    if (M2C_FIELD(arg0, u8 *, 0x9C) != 0) {
        if (func_801D2C34_641124(arg0) != 0) {
            func_801D82C0_6467B0(arg0);
            return;
        }
        func_801D2F64_641454(arg1, &D_801EE200_65C6F0, 0, 0, 8);
        func_801D2D64_641254(arg0);
        func_801D2EB0_6413A0(M2C_FIELD(arg0, f32 *, 0x64), arg0);
    }
}
