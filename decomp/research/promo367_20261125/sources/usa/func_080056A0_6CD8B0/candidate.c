#include "m2c_types.h"
extern char func_800127B8_133B8;
extern char func_80012818_13418;
extern char func_80012900_13500;
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08005768_6CD978();                     /* static */
extern void *D_801FC628_5B8538;

void func_080056A0_6CD8B0(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_800127B8_133B8)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3600000, 0x43A00000, 0x42C20000);
    ((M2C_UNK(*)())&func_80012818_13418)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43A78000, 0x431D0000);
    ((M2C_UNK(*)())&func_80012900_13500)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE);
    if (((s32(*)())&func_800240DC_24CDC)(0x165) != 0) {
        ((M2C_UNK(*)())&func_80024088_24C88)(0x165);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08005768_6CD978);
    }
}
