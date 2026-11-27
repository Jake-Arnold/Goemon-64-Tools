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

extern D_8015C5C8_t *g_system_ptr;

void func_80225068_5E05F8(s32 arg0, u8 arg1, u8 arg2, u8 arg3, u8 arg4) {
    g_system_ptr->sub->d = arg1;
    g_system_ptr->sub->e = arg2;
    g_system_ptr->sub->f = arg3;
    g_system_ptr->sub->g = arg4;
}
