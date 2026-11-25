typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
typedef struct { void * f_0; u8 pad_4[4]; f32 f_8; f32 f_C; f32 f_10; u8 pad_14[8]; f32 f_1C; f32 f_20; f32 f_24; u8 pad_28[100]; f32 f_8C; f32 f_90; f32 f_94; } RecoveredFields_var_s0;
void *func_80036158_36D58(void *, void *, M2C_UNK); /* extern */
M2C_UNK func_801E8858_5A4768(void *, M2C_UNK);      /* extern */
extern f32 D_8020B834_5C7744;

void func_801E99CC_5A58DC(void *arg0, void **arg1, s32 arg2) {
    f32 temp_f20;
    void *var_s0;

    var_s0 = *arg1;
    if (var_s0 != NULL) {
        temp_f20 = D_8020B834_5C7744;
        do {
            func_801E8858_5A4768(var_s0, 0xA);
            ((RecoveredFields_var_s0 *)var_s0)->f_1C = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_1C - temp_f20);
            ((RecoveredFields_var_s0 *)var_s0)->f_20 = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_20 - temp_f20);
            ((RecoveredFields_var_s0 *)var_s0)->f_24 = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_24 - temp_f20);
            ((RecoveredFields_var_s0 *)var_s0)->f_8 = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_8 + ((RecoveredFields_var_s0 *)var_s0)->f_8C);
            ((RecoveredFields_var_s0 *)var_s0)->f_C = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_C + ((RecoveredFields_var_s0 *)var_s0)->f_90);
            ((RecoveredFields_var_s0 *)var_s0)->f_10 = (f32) (((RecoveredFields_var_s0 *)var_s0)->f_10 + ((RecoveredFields_var_s0 *)var_s0)->f_94);
            if (((RecoveredFields_var_s0 *)var_s0)->f_1C <= 0.0f) {
                var_s0 = func_80036158_36D58(arg0, *arg1, 1);
                M2C_FIELD(arg0, u8 *, 0x61) = (u8) (M2C_FIELD(arg0, u8 *, 0x61) - 1);
                if (arg2 == 0) {
                    M2C_FIELD(arg0, s16 *, 0xAA) = 2;
                }
            } else {
                var_s0 = ((RecoveredFields_var_s0 *)var_s0)->f_0;
            }
        } while (var_s0 != NULL);
    }
}
