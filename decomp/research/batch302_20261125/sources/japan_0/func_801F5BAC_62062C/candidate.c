typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_801DBA50_6064D0(void *, f32);
void func_801FC7A4_627224(unsigned char *);
void func_801FCE00_627880(void *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK func_801F5C10_620690;

void func_801F5BAC_62062C(u8 *arg0, M2C_UNK arg1) {
    func_801FC7A4_627224(arg0);
    M2C_FIELD(arg0, f32 *, 0x74) = 8.0f;
    func_801FCE00_627880(arg0);
    if (func_801DBA50_6064D0(arg0, -110.0f) != 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 2;
        func_80034E8C_35A8C(&func_801F5C10_620690);
    }
}
