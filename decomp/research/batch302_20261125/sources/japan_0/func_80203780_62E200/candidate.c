typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_801D8604_603084(void *, void *);
void func_8020559C_63001C(unsigned char *);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
extern M2C_UNK D_80210B28_63B5A8;
extern M2C_UNK D_80210B30_63B5B0;
extern void *func_80214670_5CFC00;
extern M2C_UNK func_802037F4_62E274;

void func_80203780_62E200(u8 *arg0, void *arg1) {
    func_8020559C_63001C(arg0);
    M2C_FIELD(func_80214670_5CFC00, s8 *, 0x815) = 0;
    if ((s32) M2C_FIELD(arg1, u16 *, 0x16) < 0x201) {
        func_801D8604_603084(arg1, &D_80210B28_63B5A8);
    } else {
        func_801D8604_603084(arg1, &D_80210B30_63B5B0);
    }
    func_80034E8C_35A8C(&func_802037F4_62E274);
}
