#include "m2c_types.h"

typedef struct {
    u8 pad0[0xD0];
    s32 unkD0;
} Obj_801F1BD8;

void func_801F76D4_622154(Obj_801F1BD8 *, s32, s32);

void func_801F7308_621D88(Obj_801F1BD8 *arg0) {
    switch (arg0->unkD0) {
    case 0:
        func_801F76D4_622154(arg0, 3, 0x50);
        break;
    case 1:
    default:
        func_801F76D4_622154(arg0, 3, 0x50);
        arg0->unkD0 = 0;
        break;
    }
}
