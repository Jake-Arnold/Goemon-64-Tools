#include "m2c_types.h"
typedef struct {
    u8 pad0[0xD];
    u8 d;
    u8 e;
    u8 f;
    u8 g;
} Sub;

typedef struct {
    u8 pad0[0x3B018];
    Sub *sub;
} D_8015C5C8_t;

extern D_8015C5C8_t *D_8015C5C8_15D1C8;

void func_802202F8_5DB7C8(s32 arg0, u8 arg1, u8 arg2, u8 arg3, u8 arg4) {
    D_8015C5C8_15D1C8->sub->d = arg1;
    D_8015C5C8_15D1C8->sub->e = arg2;
    D_8015C5C8_15D1C8->sub->f = arg3;
    D_8015C5C8_15D1C8->sub->g = arg4;
}
