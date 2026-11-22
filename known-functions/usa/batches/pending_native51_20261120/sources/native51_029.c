#define NULL ((void*)0)
typedef unsigned char u8;typedef signed char s8;typedef unsigned short u16;typedef signed short s16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef signed long long s64;typedef float f32;typedef double f64;
#include "research_m2c_macros.h"
M2C_UNK func_8003522C_35E2C(void *, M2C_UNK *);     /* extern */
M2C_UNK func_801D31CC_5FE5AC(void *, M2C_UNK *);    /* extern */
M2C_UNK func_801F7004_6223E4();                     /* extern */
M2C_UNK func_801F7074_622454(void *);               /* extern */
s32 func_801F71DC_6225BC();                         /* extern */
extern M2C_UNK D_8020B260_636640;
extern M2C_UNK func_801F03C4_61B7A4;
extern M2C_UNK func_801F047C_61B85C;

void func_801F0540_61B920(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0xD8) = 0;
    M2C_FIELD(arg0, s32 *, 0xE0) = 0;
    func_801F7004_6223E4();
    func_801F7074_622454(arg0);
    func_801D31CC_5FE5AC(arg0, &D_8020B260_636640);
    if (func_801F71DC_6225BC() == 0) {
        func_8003522C_35E2C(arg0, &func_801F03C4_61B7A4);
        return;
    }
    func_8003522C_35E2C(arg0, &func_801F047C_61B85C);
}
