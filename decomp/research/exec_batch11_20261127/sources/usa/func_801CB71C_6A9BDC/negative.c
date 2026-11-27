#include "m2c_types.h"

typedef struct {
    u8 pad[0x68];
} UnkPfs;

s32 func_801CB978_6A9E38(u8);
s32 osPfsFileState(UnkPfs *, s32, void *);
extern UnkPfs D_801671F0_167DF0[];
extern u8 D_80167390[];

s32 func_801CB71C_6A9BDC(u8 arg0, s32 arg1, void *arg2) {
    if (D_80167390[arg0] == 0) {
        { *(volatile int *)0x80000000 = 1; } return osPfsFileState(&D_801671F0_167DF0[arg0], arg1, arg2);
    }
    return func_801CB978_6A9E38(arg0);
}
