#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003521C_35E1C(M2C_UNK *);             /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F76D0_622AB0();                     /* extern */
extern M2C_UNK D_8020B270_636650;
extern M2C_UNK func_801F0A50_61BE30;

void func_801F1690_61CA70(void *arg0, M2C_UNK arg1) {
    func_801F76D0_622AB0();
    func_801D31CC_5FE5AC(arg0, &D_8020B270_636650);
    M2C_FIELD(arg0, f32 *, 0x74) = 1.0f;
    func_8003521C_35E1C(&func_801F0A50_61BE30);
}
