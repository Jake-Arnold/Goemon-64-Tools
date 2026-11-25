typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((s8 *)0)
void func_801F45D0_61F050(s32);
void func_801D8604_603084(s8 *, s8 *);
void func_801F4584_61F004(s32);
void func_801DBC28_6066A8(s8 *, f32);
s32 func_801D9A58_6044D8(s32, s32);
M2C_UNK func_80034E8C_35A8C(M2C_UNK *);             /* extern */
f32 func_801D8910_603390(s8 *, M2C_UNK);          /* extern */
M2C_UNK func_801DC97C_6073FC(s8 *, M2C_UNK);      /* extern */
extern M2C_UNK D_802108A0_63B320;
extern M2C_UNK func_801EAA08_615488;

void func_801ED114_617B94(s8 *arg0, s8 *arg1) {
    volatile int negative_control = 1;

    M2C_FIELD(arg0, s32 *, 0xB0) = 1;
    if (M2C_FIELD(arg0, s32 *, 0x90) == 0) {
        func_801DBC28_6066A8(arg0, -1.0f);
        func_801DC97C_6073FC(arg0 + 0x74, 0x41100000);
        if (func_801D9A58_6044D8((s32) arg0, -0x3DCC0000) != 0) {
            M2C_FIELD(arg0, s32 *, 0x90) = 1;
        }
    } else {
        func_801F4584_61F004((s32) arg0);
        func_801F45D0_61F050((s32) arg0);
    }
    if ((func_801D8910_603390(arg0, 0xC2C80000) == 0.0f) && (M2C_FIELD(arg0, s32 *, 0x90) != 0)) {
        func_801D8604_603084(arg1, &D_802108A0_63B320);
        func_80034E8C_35A8C(&func_801EAA08_615488);
    }
}
