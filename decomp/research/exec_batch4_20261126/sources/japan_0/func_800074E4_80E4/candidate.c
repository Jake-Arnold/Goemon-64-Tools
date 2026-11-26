#include "m2c_types.h"
typedef struct Node {
    struct Node *next;
    s32 unk4;
    s32 unk8;
    s32 unkC;
    s32 unk10;
} Node;

typedef struct {
    u8 pad0[0x29C];
    Node *unk29C;
    Node *unk2A0;
    Node *unk2A4;
    Node *unk2A8;
    u8 pad2AC[0xC];
    s32 unk2B8;
} ListContainer;

void func_800074E4_80E4(ListContainer *arg0, Node *arg1) {
    register s32 type = arg1->unk10;
    if (type == 2) {
        if (arg0->unk2A4 != NULL) {
            arg0->unk2A4->next = arg1;
        } else {
            arg0->unk29C = arg1;
        }
        arg0->unk2A4 = arg1;
        arg0->unk2B8 = 1;
    } else {
        if (arg0->unk2A8 != NULL) {
            arg0->unk2A8->next = arg1;
        } else {
            arg0->unk2A0 = arg1;
        }
        arg0->unk2A8 = arg1;
    }
    arg1->next = NULL;
    arg1->unk4 = arg1->unk8 & 3;
}
