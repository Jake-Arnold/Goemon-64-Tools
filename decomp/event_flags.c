/* Reconstructed from the verified US ROM, translation unit ROM 0x249F0.
 * Original symbol names retained for comparison with pinned mnsg.
 * These are unchecked engine routines, not public safe editing APIs.
 */
#include "common.h"

extern u8 D_80168E90_169A90[];
extern u8 D_80168EF4_169AF4[];
extern u8 D_80168EF8_169AF8[];
extern u8 D_80168F5C_169B5C[];
extern u8 D_8015C608_15D208[];
extern u8 D_8015C66C_15D26C[];

void func_80023DF0_249F0(s32 flag) {
    u8 *byte;
    byte = D_80168E90_169A90 + (u8)(flag / 8);
    *byte |= (u8)(1 << (u8)(flag % 8));
}

void func_80023E40_24A40(s32 flag) {
    u8 *byte;
    byte = D_80168E90_169A90 + (u8)(flag / 8);
    *byte &= ~((u8)(1 << (u8)(flag % 8)));
}

s32 func_80023E94_24A94(s32 flag) {
    return D_80168E90_169A90[(u8)(flag / 8)] & ((u8)(1 << (u8)(flag % 8))) & 0xFF;
}

void func_80023EE4_24AE4(void) {
    s32 index;
    for (index = 0; index < 0x64; index++) {
        D_80168E90_169A90[index] = 0;
    }
}

void func_80023F14_24B14(s32 flag) {
    u8 *byte;
    byte = D_80168EF8_169AF8 + (u8)(flag / 8);
    *byte |= (u8)(1 << (u8)(flag % 8));
}

void func_80023F64_24B64(s32 flag) {
    u8 *byte;
    byte = D_80168EF8_169AF8 + (u8)(flag / 8);
    *byte &= ~((u8)(1 << (u8)(flag % 8)));
}

s32 func_80023FB8_24BB8(s32 flag) {
    return D_80168EF8_169AF8[(u8)(flag / 8)] & ((u8)(1 << (u8)(flag % 8))) & 0xFF;
}

void func_80024008_24C08(void) {
    s32 index;
    for (index = 0; index < 0x64; index++) {
        D_80168EF8_169AF8[index] = 0;
    }
}

void func_80024038_24C38(s32 flag) {
    u8 *byte;
    byte = D_8015C608_15D208 + (u8)(flag / 8);
    *byte |= (u8)(1 << (u8)(flag % 8));
}

void func_80024088_24C88(s32 flag) {
    u8 *byte;
    byte = D_8015C608_15D208 + (u8)(flag / 8);
    *byte &= ~((u8)(1 << (u8)(flag % 8)));
}

s32 func_800240DC_24CDC(s32 flag) {
    return D_8015C608_15D208[(u8)(flag / 8)] & ((u8)(1 << (u8)(flag % 8))) & 0xFF;
}

void func_8002412C_24D2C(void) {
    s32 index;
    for (index = 0; index < 0x64; index++) {
        D_8015C608_15D208[index] = 0;
    }
}
