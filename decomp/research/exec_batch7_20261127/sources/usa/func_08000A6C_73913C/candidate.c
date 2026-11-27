#include "m2c_types.h"

void func_80034EF8_35AF8(void);

typedef struct {
    u8 pad0[0xAE20];
    u8 unkAE20;
    u8 unkAE21;
    u8 unkAE22;
} Struct_08000A6C;

extern Struct_08000A6C D_800BCCC0_BD8C0;

void func_08000A6C_73913C(void) {
    void (*fn)(void) = func_80034EF8_35AF8;
    fn();
    D_800BCCC0_BD8C0.unkAE22 = 0;
    D_800BCCC0_BD8C0.unkAE20 = 0;
}
