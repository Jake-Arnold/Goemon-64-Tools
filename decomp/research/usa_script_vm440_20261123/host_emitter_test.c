#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sources/func_8003E234_3EE34.c"
static Gfx guarded[13];
static VmState vm_state;
u8 D_80077150_77D50, D_800777F0_783F0;
VmState *D_80077860_78460=&vm_state;
Gfx *D_8015C5CC_15D1CC;
s32 D_801C78D8_1C84D8,D_801C78DC_1C84DC;
static uint32_t rnd=0xF1A5CC45U;
static uint32_t next(void){rnd^=rnd<<13;rnd^=rnd>>17;rnd^=rnd<<5;return rnd;}
static uint32_t pack(uint32_t x,uint32_t y){return ((x*4U&0xfffU)<<12)|(y*4U&0xfffU);}
int main(void){
    for(unsigned i=0;i<4096;i++){
        uint32_t x=next(),y=next();uint8_t b=(uint8_t)i;
        if(i<8){static const uint32_t edge[]={0,1,0x3ff,0x400,0x7fffffff,0x80000000,0xfffffffe,0xffffffff};x=edge[i];y=edge[7-i];}
        memcpy(&D_801C78D8_1C84D8,&x,4);memcpy(&D_801C78DC_1C84DC,&y,4);vm_state.field5D=b;
        memset(guarded,0xA5,sizeof guarded);D_8015C5CC_15D1CC=guarded+1;
        func_8003E234_3EE34();
        Gfx expected[11]={{0x06000000,(uint32_t)(uintptr_t)&D_800777F0_783F0},{0xFD100000,(uint32_t)(uintptr_t)&D_80077150_77D50},{0xF5100000,0x07000000},{0xE6000000,0},{0xF3000000,0x071FF100},{0xE7000000,0},{0xF5101000,0},{0xF2000000,0x7C03C},{0xE4000000|pack(x+15U,y+15U),pack(x,y)},{0xB4000000,(uint32_t)(b&1U)<<25},{0xB3000000,0x10000400}};
        if(D_8015C5CC_15D1CC!=guarded+12||memcmp(guarded+1,expected,sizeof expected)||guarded[0].w0!=0xA5A5A5A5||guarded[0].w1!=0xA5A5A5A5||guarded[12].w0!=0xA5A5A5A5||guarded[12].w1!=0xA5A5A5A5){fprintf(stderr,"failed case %u\n",i);return 1;}
    }
    puts("PASS 4096 actual-source emitter cases");return 0;
}
