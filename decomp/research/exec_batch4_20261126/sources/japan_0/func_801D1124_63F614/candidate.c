#include "m2c_types.h"
void func_800371B8_37DB8(void);

typedef struct {
    u8 pad0[6];
    s16 unk6;
} Sub801CB9F4;

typedef struct {
    u8 pad0[0xEC];
    Sub801CB9F4 *unkEC;
} Struct801CB9F4;

void func_801D1124_63F614(Struct801CB9F4 *arg0, s16 arg1) {
    s16 temp_v0;
    Sub801CB9F4 *temp_v1;

    temp_v1 = arg0->unkEC;
    temp_v0 = temp_v1->unk6;
    if (temp_v0 != 0) {
        temp_v0--;
        temp_v1->unk6 = temp_v0;
        if (temp_v0 != 0) {
            func_800371B8_37DB8();
        }
    }
}
