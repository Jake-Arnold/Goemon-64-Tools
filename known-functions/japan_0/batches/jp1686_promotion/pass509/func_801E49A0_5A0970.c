#include "m2c_types.h"
M2C_UNK func_801E01C8_59C198(s32, M2C_UNK);         /* extern */
M2C_UNK func_801E2AD0_59EAA0(s32, M2C_UNK);         /* extern */
s32 func_801E70B8_5A3088(s32);                      /* extern */
M2C_UNK func_801E8424_5A43F4(s32);                  /* extern */
M2C_UNK func_801ED058_5A9028();                     /* extern */
s32 func_801E4B28_5A0AF8(s32);                      /* static */
s32 func_801E4B88_5A0B58(s32);                      /* static */

void func_801E49A0_5A0970(s32 arg0, M2C_UNK arg1) {
    func_801ED058_5A9028();
    func_801E2AD0_59EAA0(arg0, 0xF);
    func_801E8424_5A43F4(arg0);
    if ((func_801E4B28_5A0AF8(arg0) == 0) && (func_801E4B88_5A0B58(arg0) == 0) && (func_801E70B8_5A3088(arg0) == 0)) {
        func_801E01C8_59C198(arg0, 0x45);
    }
}
