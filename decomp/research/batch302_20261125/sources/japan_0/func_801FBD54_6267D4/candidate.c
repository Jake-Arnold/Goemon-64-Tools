typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D8604_603084(void *, void *);
void func_801FC7A4_627224(unsigned char *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK D_80210A00_63B480;
extern M2C_UNK func_801FBD90_626810;

void func_801FBD54_6267D4(u8 *arg0, void *arg1) {
    func_801FC7A4_627224(arg0);
    func_801D8604_603084(arg1, &D_80210A00_63B480);
    func_80034E8C_35A8C(&func_801FBD90_626810);
}
