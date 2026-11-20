#include "m2c_types.h"
M2C_UNK osCreateThread(M2C_UNK *, M2C_UNK, M2C_UNK *, M2C_UNK, M2C_UNK *, s32); /* extern */
M2C_UNK osInitialize();                             /* extern */
M2C_UNK osStartThread(M2C_UNK *);                   /* extern */
extern M2C_UNK func_800004AC_10AC;
extern M2C_UNK g_idle_thread;
extern M2C_UNK g_main_thread;

void func_80000450_1050(void) {
    osInitialize();
    osCreateThread(&g_idle_thread, 1, &func_800004AC_10AC, 0, &g_main_thread, 9);
    osStartThread(&g_idle_thread);
}
