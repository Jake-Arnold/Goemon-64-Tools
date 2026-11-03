#include "object_flags.h"
ObjectFlagNode *func_800362DC_36EDC(ObjectFlagOwner *arg0) {
    ObjectFlagNode *v = arg0->list;
    while (v) { v->flags |= 0x80; v = v->next; }
    return v;
}
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_80036308_36F08.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_80036388_36F88.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_800363F4_36FF4.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/object_flags/func_80036448_37048.s")
