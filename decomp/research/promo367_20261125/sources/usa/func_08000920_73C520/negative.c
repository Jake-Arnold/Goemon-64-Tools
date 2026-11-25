#include "../m2c_types.h"
extern char func_80013400_14000;
extern char func_80034EF8_35AF8;

s32 func_08000920_73C520(void *arg0) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_80013400_14000)(M2C_FIELD(arg0, s32 *, 0x68), M2C_FIELD(arg0, u8 *, 0x6C), M2C_FIELD(arg0, u8 *, 0x6D), M2C_FIELD(arg0, u8 *, 0x6E));
    ((M2C_UNK(*)())&func_80034EF8_35AF8)(arg0);
    return 0;
}
