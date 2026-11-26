#include "m2c_types.h"
typedef struct {
    u8 pad[0xC];
    u8 unk_C;
} Unk3BC80_C;
extern Unk3BC80_C *D_801C1728_1C2328;
extern u8 *D_801C172C_1C232C;

void func_8003CCCC_3D8CC(void) {
    D_801C1728_1C2328->unk_C = *D_801C172C_1C232C;
    D_801C172C_1C232C++;
}
