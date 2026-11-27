#include "m2c_types.h"

typedef struct Node_1EF4A8 {
    struct Node_1EF4A8 *next;
    u8 pad4[0x8C];
    u8 unk90;
} Node_1EF4A8;

typedef struct {
    u8 pad0[0x18];
    Node_1EF4A8 *unk18;
} Res_1EF4A8;

typedef struct {
    u8 pad0[0x5C];
    s32 unk5C;
} Arg_1EF4A8;

Res_1EF4A8 *func_801EDDF0_5A9DC0(s32, s32);

Node_1EF4A8 *func_801F44C8_5B0498(Arg_1EF4A8 *arg0, u16 arg1) {
    Res_1EF4A8 *res = func_801EDDF0_5A9DC0(arg0->unk5C, 0x1C);
    Node_1EF4A8 *node;
    s32 i;

    if (res == NULL) {
        return NULL;
    }
    node = res->unk18;
    if (node == NULL) {
        return NULL;
    }
    for (i = 0; i < 3; i++, node = node->next) {
        if (i == arg1 && node->unk90 != 0) {
            return node;
        }
    }
    return NULL;
}
