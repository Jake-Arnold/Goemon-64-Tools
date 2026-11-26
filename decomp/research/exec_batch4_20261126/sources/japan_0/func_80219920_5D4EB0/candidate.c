#include "m2c_types.h"
extern s32 D_801CCE70_1CDA70;
extern void *D_80201538_5BD508;

void func_80219920_5D4EB0(void) {
    void *ptr = (void *)(M2C_FIELD(D_80201538_5BD508, u32 *, 0x2C) & 0x8FFFFFFE);
    M2C_FIELD(ptr, s16 *, 0x1A) = (s16) (D_801CCE70_1CDA70 * 4);
}
