#include "m2c_types.h"
extern char func_80023D9C_2499C;

void func_08006608_6BE388(void *arg0, M2C_UNK arg1) {
    if (((s32(*)())&func_80023D9C_2499C)(0x12E) != 0) {
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) | 2);
    }
}
