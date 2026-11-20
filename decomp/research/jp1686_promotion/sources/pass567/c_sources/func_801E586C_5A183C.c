#include "../m2c_types.h"
M2C_UNK func_801E01C8_59C198(s32, M2C_UNK);         /* extern */
s32 func_801EC488_5A8458();                         /* extern */
extern s32 D_802016D4_5BD6A4;

void func_801E586C_5A183C(s32 arg0, M2C_UNK arg1) {
    D_802016D4_5BD6A4 = 0;
    if (func_801EC488_5A8458() != 0) {
        func_801E01C8_59C198(arg0, 0x3A);
    }
}
