/* RESEARCH_ONLY: independently IDO 5.3 byte-matched original gameplay Start handler.
   NOT G2-promoted. No ROM, assembly, or proprietary compiler included. */
typedef int s32;typedef unsigned short u16;typedef unsigned char u8;typedef signed char s8;typedef int M2C_UNK;
typedef struct Sys {
char pad_0[0x3ADE0];
s8 phase;
s8 phase_b;
char pad_3ADE2[0x2];
u8 submode;
char pad_3ADE5[0x31];
u16 condition;
char pad_3AE18[0xE];
u16 pause_latch;
char pad_3AE28[0x1];
u8 local_gate;
char pad_3AE2A[0x252];
u16 pressed;
char pad_3B07E[0x9480F];
u8 external_b;
char pad_CF88E[0x14];
u8 external_a;
} Sys;
extern Sys g_system;

M2C_UNK func_8000B654_C254();                       /* extern */
M2C_UNK func_8001F750_20350();                      /* extern */
M2C_UNK func_80038838_39438(M2C_UNK);               /* extern */
s32 func_8003EE44_3FA44();                          /* extern */


void func_8001F610_20210(void) {
    func_8000B654_C254();
    if (g_system.pause_latch == 0) {
        if ((*((u16*)((u8*)&g_system + 0x3B07C)) & 0x1000) && (g_system.local_gate == 0) && (g_system.submode != 3) && ((s32) g_system.submode < 4) && (func_8003EE44_3FA44() == 0) && (g_system.external_a == 0) && (g_system.local_gate == 0) && (g_system.external_b == 0) && (g_system.condition == 0)) {
            g_system.pause_latch = 1U;
            g_system.phase = 0;
            g_system.phase_b = 0;
            func_80038838_39438(3);
        }
    } else {
        func_8001F750_20350();
    }
}
