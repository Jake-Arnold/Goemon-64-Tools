#include "m2c_types.h"

typedef struct {
    u8 pad0[0xD0];
    s32 unkD0;
} Obj_801F1BD8;

void func_801F1FA4_61D384(Obj_801F1BD8 *, s32, s32);

void func_801F1BD8_61CFB8(Obj_801F1BD8 *arg0) {
    switch (arg0->unkD0) {
    case 0:
        func_801F1FA4_61D384(arg0, 3, 0x50);
        break;
    case 1:
    default:
        func_801F1FA4_61D384(arg0, 3, 0x50);
        arg0->unkD0 = 0;
        break;
    }
}
