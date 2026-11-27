typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DDF0_E9F0(void *, M2C_UNK *, M2C_UNK, M2C_UNK, s32, s32);
M2C_UNK func_80035020_35C20();
void *func_80035854_36454(M2C_UNK *, s32, M2C_UNK, s32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
M2C_UNK func_801D609C_60147C();
M2C_UNK func_801D60B4_601494(void *);
extern M2C_UNK D_8020A3A8_635788;
extern M2C_UNK func_801EB790_616B70;

void func_801EB628_616A08(void *arg0, void *arg1) {
    s32 temp_t2;
    s32 temp_t5;
    void *temp_s0;
    void *temp_v0;

    func_801D609C_60147C();
    func_801D60B4_601494(arg0);
    M2C_FIELD(arg0, s32 *, 0x90) = (s32) (M2C_FIELD(arg0, s32 *, 0x90) - 6);
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (func_8000DDF0_E9F0(arg0, &D_8020A3A8_635788, 0xFF, 0, 0, M2C_FIELD(arg0, s32 *, 0x90)) | 0x40000000 | 0x20000000);

    if ((M2C_FIELD(arg0, s32 *, 0x80) -= 1) == 0) {
        func_80035020_35C20();
        return;
    }

    if ((M2C_FIELD(arg0, s32 *, 0x7C) -= 1) <= 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 8;
        temp_v0 = func_80035854_36454(&func_801EB790_616B70, M2C_FIELD(arg1, s32 *, 0x2C), 0, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0x8000, 0x8000, 0x8000, M2C_FIELD(arg1, f32 *, 0x1C), M2C_FIELD(arg1, f32 *, 0x20), M2C_FIELD(arg1, f32 *, 0x24), 0x4B0, 0);
        if (temp_v0 != NULL) {
            temp_s0 = M2C_FIELD(temp_v0, void **, 0x18);
            M2C_FIELD(temp_v0, s32 *, 0x90) = 0xB4;
            M2C_FIELD(temp_s0, s8 *, 5) = 9;
            M2C_FIELD(temp_s0, s32 *, 0x30) = (s32) (func_8000DDF0_E9F0(temp_v0, &D_8020A3A8_635788, 0xFF, 0, 0, M2C_FIELD(temp_v0, s32 *, 0x90)) | 0x40000000 | 0x20000000);
        }
    }
}
