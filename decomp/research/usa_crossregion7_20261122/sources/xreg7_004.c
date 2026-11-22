#include "probe_common.h"
M2C_UNK func_801E307C_59EF8C();                     /* static */

void func_801DD458_599368(void *arg0) {
    func_801E307C_59EF8C();
    *M2C_FIELD(arg0, s16 **, 0x5C) = 1;
    M2C_FIELD(arg0, s8 *, 0xD4) = 0;
    M2C_FIELD(arg0, u8 *, 0x30) = (u8) (M2C_FIELD(arg0, u8 *, 0x30) & 0xFFFE);
}
