typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
s32 func_8000DBB0_E7B0(void *, M2C_UNK *, M2C_UNK, M2C_UNK, s32, s32);
M2C_UNK func_80034C90_35890();
void *func_800354C4_360C4(M2C_UNK *, s32, M2C_UNK, s32, f32, f32, s32, s32, s32, f32, f32, f32, s32, s32);
M2C_UNK func_801DB7BC_60623C();
M2C_UNK func_801DB7D4_606254(void *);
extern M2C_UNK D_8020FAD8_63A558;
extern M2C_UNK func_801F0EC0_61B940;

void func_801F0D58_61B7D8(void *arg0, void *arg1) {
    s32 temp_t2;
    s32 temp_t5;
    void *temp_s0;
    void *temp_v0;

    func_801DB7BC_60623C();
    func_801DB7D4_606254(arg0);
    M2C_FIELD(arg0, s32 *, 0x90) = (s32) (M2C_FIELD(arg0, s32 *, 0x90) - 6);
    M2C_FIELD(arg1, s32 *, 0x30) = (s32) (func_8000DBB0_E7B0(arg0, &D_8020FAD8_63A558, 0xFF, 0, 0, M2C_FIELD(arg0, s32 *, 0x90)) | 0x40000000 | 0x20000000);

    if ((M2C_FIELD(arg0, s32 *, 0x80) -= 1) == 0) {
        func_80034C90_35890();
        return;
    }

    if ((M2C_FIELD(arg0, s32 *, 0x7C) -= 1) <= 0) {
        M2C_FIELD(arg0, s32 *, 0x7C) = 8;
        temp_v0 = func_800354C4_360C4(&func_801F0EC0_61B940, M2C_FIELD(arg1, s32 *, 0x2C), 0, M2C_FIELD(arg1, s32 *, 8), M2C_FIELD(arg1, f32 *, 0xC), M2C_FIELD(arg1, f32 *, 0x10), 0x8000, 0x8000, 0x8000, M2C_FIELD(arg1, f32 *, 0x1C), M2C_FIELD(arg1, f32 *, 0x20), M2C_FIELD(arg1, f32 *, 0x24), 0x4B0, 0);
        if (temp_v0 != NULL) {
            temp_s0 = M2C_FIELD(temp_v0, void **, 0x18);
            M2C_FIELD(temp_v0, s32 *, 0x90) = 0xB4;
            M2C_FIELD(temp_s0, s8 *, 5) = 9;
            M2C_FIELD(temp_s0, s32 *, 0x30) = (s32) (func_8000DBB0_E7B0(temp_v0, &D_8020FAD8_63A558, 0xFF, 0, 0, M2C_FIELD(temp_v0, s32 *, 0x90)) | 0x40000000 | 0x20000000);
        }
    }
}
