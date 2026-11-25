typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
void func_80034E8C_35A8C(s32);
s32 func_801D9238_603CB8(void *, f32, u16);
void func_801D9620_6040A0(void *, u16, s32);
void func_801DBC28_6066A8(void *, f32);
extern M2C_UNK func_801F824C_622CCC;

void func_801F81C8_622C48(void *arg0, void *arg1) {
    func_801D9238_603CB8(arg0, M2C_FIELD(arg1, f32 *, 0x20) * 300.0f, 0x10U);
    func_801D9620_6040A0(arg0, 0U, 8);
    func_801DBC28_6066A8(arg0, -0.3f);
    if (M2C_FIELD(arg0, f32 *, 0x74) <= 0.0f) {
        func_80034E8C_35A8C((s32) &func_801F824C_622CCC);
    }
}
