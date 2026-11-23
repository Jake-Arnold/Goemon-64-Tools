typedef unsigned char u8; typedef struct { u8 pad[0x3ADDE]; u8 phase; u8 state; } System;
extern System *g_system_ptr; extern void func_800032A4_3EA4(int);
void func_8000339C_3F9C(void) { g_system_ptr->phase++; g_system_ptr->state = 0; func_800032A4_3EA4(0); }
