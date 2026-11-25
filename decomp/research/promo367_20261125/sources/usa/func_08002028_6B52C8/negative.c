#include "m2c_types.h"
extern char func_8003521C_35E1C;
extern char func_8021927C_5D474C;
extern char func_802197D8_5D4CA8;
extern M2C_UNK func_080020D8_6B5378;
extern M2C_UNK func_080024A0_6B5740;
extern M2C_UNK func_080028A4_6B5B44;

void func_08002028_6B52C8(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    s32 temp_v0;

    ((M2C_UNK(*)())&func_8021927C_5D474C)();
    ((M2C_UNK(*)())&func_802197D8_5D4CA8)(arg0, 8);
    temp_v0 = M2C_FIELD(arg0, u8 *, 0x8D);
    if ((s32) temp_v0 >= 9) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080020D8_6B5378);
        return;
    }
    if ((s32) temp_v0 >= 5) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080024A0_6B5740);
        return;
    }
    if ((s32) temp_v0 >= 2) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080028A4_6B5B44);
    }
}
