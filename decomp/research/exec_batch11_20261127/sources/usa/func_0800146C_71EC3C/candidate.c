#include "m2c_types.h"
extern u8 func_80014B74_15774[];
extern u8 func_80034EF8_35AF8[];
extern s32 D_8015C5C8_15D1C8;

s32 func_0800146C_71EC3C(void *arg0) {
    if (M2C_FIELD(arg0, void **, 0x74) != NULL) {
        ((M2C_UNK (*)(s32, s32, void *))func_80014B74_15774)(D_8015C5C8_15D1C8 + 0xC7FA4, M2C_FIELD(arg0, s32 *, 0x74), arg0);
    }
    ((M2C_UNK (*)(void *))func_80034EF8_35AF8)(arg0);
    return 0;
}
