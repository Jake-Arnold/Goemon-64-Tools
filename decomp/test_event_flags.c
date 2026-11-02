/* Host semantic tests against synthetic banks, never emulator/game RAM. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "common.h"

u8 D_80168E90_169A90[0x100];
u8 D_80168EF8_169AF8[0x100];
u8 D_8015C608_15D208[0x100];

void func_80023DF0_249F0(s32);
void func_80023E40_24A40(s32);
s32 func_80023E94_24A94(s32);
void func_80023EE4_24AE4(void);
void func_80023F14_24B14(s32);
void func_80023F64_24B64(s32);
s32 func_80023FB8_24BB8(s32);
void func_80024008_24C08(void);
void func_80024038_24C38(s32);
void func_80024088_24C88(s32);
s32 func_800240DC_24CDC(s32);
void func_8002412C_24D2C(void);

struct Bank {
    u8 *bytes;
    void (*set)(s32);
    void (*clear)(s32);
    s32 (*test)(s32);
    void (*reset)(void);
};

int main(void) {
    struct Bank banks[] = {
        {D_80168E90_169A90, func_80023DF0_249F0, func_80023E40_24A40, func_80023E94_24A94, func_80023EE4_24AE4},
        {D_80168EF8_169AF8, func_80023F14_24B14, func_80023F64_24B64, func_80023FB8_24BB8, func_80024008_24C08},
        {D_8015C608_15D208, func_80024038_24C38, func_80024088_24C88, func_800240DC_24CDC, func_8002412C_24D2C}
    };
    unsigned bank, flag, i, other;
    for (bank = 0; bank < 3; bank++) {
        for (flag = 0; flag < 800; flag++) {
            unsigned index = flag >> 3;
            u8 mask = (u8)(1u << (flag & 7));
            for (other = 0; other < 3; other++) memset(banks[other].bytes, 0xA5, 0x100);
            assert(banks[bank].test((s32)flag) == (0xA5 & mask));
            banks[bank].set((s32)flag);
            banks[bank].set((s32)flag); /* Setting is idempotent, not arithmetic addition. */
            assert(banks[bank].test((s32)flag) == mask); /* Returns the mask, not boolean 1. */
            for (i = 0; i < 0x100; i++) assert(banks[bank].bytes[i] == (i == index ? (0xA5 | mask) : 0xA5));
            banks[bank].clear((s32)flag);
            banks[bank].clear((s32)flag);
            assert(banks[bank].test((s32)flag) == 0);
            for (i = 0; i < 0x100; i++) assert(banks[bank].bytes[i] == (i == index ? (0xA5 & (u8)~mask) : 0xA5));
            for (other = 0; other < 3; other++) {
                if (other != bank) for (i = 0; i < 0x100; i++) assert(banks[other].bytes[i] == 0xA5);
            }
        }
        for (other = 0; other < 3; other++) memset(banks[other].bytes, 0xA5, 0x100);
        banks[bank].reset();
        for (other = 0; other < 3; other++) {
            for (i = 0; i < 0x100; i++) assert(banks[other].bytes[i] == (other == bank && i < 100 ? 0 : 0xA5));
        }
    }
    puts("All 800 flags across three synthetic banks passed; clear bounds and isolation passed.");
    return 0;
}
