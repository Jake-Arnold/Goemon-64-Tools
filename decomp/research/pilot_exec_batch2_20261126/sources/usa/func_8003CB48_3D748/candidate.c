#include "m2c_types.h"
typedef struct {
    u8 pad[0x6C];
    s32 unk_6C;
} Unk3BC80;
extern Unk3BC80 *D_801C1728_1C2328;
extern s32 D_801C172C_1C232C;

void func_8003CB48_3D748(void) {
    D_801C172C_1C232C = D_801C1728_1C2328->unk_6C;
}
