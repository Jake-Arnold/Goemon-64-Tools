typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034C90_35890(void);
void func_801DB86C_6062EC(void *);
void func_80209214_633C94(void *);
void func_80209184_633C04(void *arg0, void *arg1) {
    s32 temp_t7;

    func_801DB86C_6062EC(arg0);
    if (M2C_FIELD(arg0, f32 *, 0x78) < 0.0f) {
        if (--M2C_FIELD(arg0, s32 *, 0x7C) < 0) {
            func_80034C90_35890();
            return;
        }
    }
    if (M2C_FIELD(arg1, f32 *, 0x10) > 0.0f) {
        func_80034C90_35890();
        return;
    }
    func_80209214_633C94(arg0);
}
