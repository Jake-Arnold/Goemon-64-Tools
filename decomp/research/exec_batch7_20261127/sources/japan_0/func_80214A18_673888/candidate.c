#include "m2c_types.h"

typedef struct Struct_8020FBF8 Struct_8020FBF8;

typedef struct {
    u8 pad0[0x30];
    Struct_8020FBF8 *unk30;
} SubStruct_8020FBF8;

struct Struct_8020FBF8 {
    u8 pad0[0x5C];
    SubStruct_8020FBF8 unk5C;
};

void func_800112EC_11EEC(Struct_8020FBF8 *);

void func_80214A18_673888(Struct_8020FBF8 *arg0) {
    SubStruct_8020FBF8 *sub;

    while (1) {
        sub = &arg0->unk5C;
        func_800112EC_11EEC(arg0);
        if (sub->unk30 == NULL) {
            break;
        }
        arg0 = sub->unk30;
    }
}
