#include "m2c_types.h"
typedef struct {
    u8 pad[0xAE20];
    s8 unkAE20;
    u8 pad2;
    s8 unkAE22;
} UnkBCCC0;

extern void func_80034EF8_35AF8(void);
extern UnkBCCC0 D_800BCCC0_BD8C0;

void func_08000D40_7305D0(void) {
    void (*fn)(void) = func_80034EF8_35AF8;
    fn();
    D_800BCCC0_BD8C0.unkAE22 = 0;
    D_800BCCC0_BD8C0.unkAE20 = 0;

    *(volatile s32 *)0x80000000 = 1;
}
