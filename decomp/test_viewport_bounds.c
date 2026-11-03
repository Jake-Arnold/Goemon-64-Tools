#include "common.h"
#include <assert.h>

s32 D_8006D158_6DD58, D_8006D15C_6DD5C, D_8006D160_6DD60, D_8006D164_6DD64;
s32 func_800216B0_222B0(s32,s32,s32,s32);

static void rejected(s32 left,s32 top,s32 right,s32 bottom) {
    D_8006D158_6DD58=11; D_8006D15C_6DD5C=22;
    D_8006D160_6DD60=33; D_8006D164_6DD64=44;
    assert(func_800216B0_222B0(left,top,right,bottom)==0);
    assert(D_8006D158_6DD58==11 && D_8006D15C_6DD5C==22);
    assert(D_8006D160_6DD60==33 && D_8006D164_6DD64==44);
}

int main(void) {
    assert(func_800216B0_222B0(0,0,320,240)==1);
    assert(D_8006D158_6DD58==0 && D_8006D15C_6DD5C==0);
    assert(D_8006D160_6DD60==320 && D_8006D164_6DD64==240);
    assert(func_800216B0_222B0(7,9,7,9)==1); /* Equal bounds are accepted. */
    assert(D_8006D158_6DD58==7 && D_8006D15C_6DD5C==9);
    assert(D_8006D160_6DD60==7 && D_8006D164_6DD64==9);
    rejected(-1,0,320,240); rejected(0,-1,320,240);
    rejected(0,0,321,240); rejected(0,0,320,241);
    rejected(10,0,9,240); rejected(0,10,320,9);
    rejected(0,0,-1,240); rejected(0,0,320,-1);
    return 0;
}
