#include "object_flags.h"
ObjectFlagNode *func_800362DC_36EDC(ObjectFlagOwner *arg0) {
    ObjectFlagNode *v = arg0->list;
    while (v) { v->flags |= 0x80; v = v->next; }
    return v;
}
extern void func_80007C90_8890(ObjectFlagNode *);
extern void func_8000A228_AE28(ObjectFlagNode *);
extern void func_8000A5C4_B1C4(ObjectFlagNode *);
extern void func_8000A394_AF94(ObjectFlagNode *);

void func_80036308_36F08(ObjectFlagNode *node) {
    if (node == 0) {
        return;
    }
    switch (node->flags & 0x7F) {
    case 1:
        func_80007C90_8890(node);
        func_8000A228_AE28(node);
        break;
    case 2:
        func_8000A5C4_B1C4(node);
        break;
    case 3:
        func_8000A394_AF94(node);
        break;
    case 4:
        break;
    default:
        break;
    }
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_80036388_36F88.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_800363F4_36FF4.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_80036448_37048.s")
