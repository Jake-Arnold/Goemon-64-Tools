#include "../m2c_types.h"
extern s32 D_801CD01C_1CDC1C;
extern s32 D_801CD020_1CDC20;

s32 func_8003DAB8_3E6B8(s32 arg0) {
    if (arg0 < 0) {
        return arg0;
    }
    if (D_801CD01C_1CDC1C != -1) {
        return arg0 + D_801CD020_1CDC20;
    }
    return arg0;
}
