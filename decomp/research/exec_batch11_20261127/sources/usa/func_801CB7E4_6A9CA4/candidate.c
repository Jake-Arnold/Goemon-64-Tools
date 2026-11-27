#include "m2c_types.h"

typedef struct {
    u8 pad[0x68];
} UnkPfs;

s32 func_801CB978_6A9E38(u8);
s32 osPfsFreeBlocks(UnkPfs *, s32 *);
extern UnkPfs D_801671F0_167DF0[];
extern u8 D_80167390[];

s32 func_801CB7E4_6A9CA4(u8 arg0, s32 *arg1) {
    if (D_80167390[arg0] == 0) {
        return osPfsFreeBlocks(&D_801671F0_167DF0[arg0], arg1);
    }
    return func_801CB978_6A9E38(arg0);
}
