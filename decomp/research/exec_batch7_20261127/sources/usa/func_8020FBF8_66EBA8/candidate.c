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

void func_80011760_12360(Struct_8020FBF8 *);

void func_8020FBF8_66EBA8(Struct_8020FBF8 *arg0) {
    SubStruct_8020FBF8 *sub;

    while (1) {
        sub = &arg0->unk5C;
        func_80011760_12360(arg0);
        if (sub->unk30 == NULL) {
            break;
        }
        arg0 = sub->unk30;
    }
}
