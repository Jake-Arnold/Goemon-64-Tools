/* Exercises the actual native-matching C source on the host. Host ABI is NOT N64 o32. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "../source/func_8003EBAC_3F7AC.c"

u8 D_80076148_76D48 = 0;
u8 D_800777F0_783F0 = 0;
VmState private_vm;
VmState *D_80077860_78460 = &private_vm;
Gfx commands[12];
Gfx *D_8015C5CC_15D1CC = commands;
static uint32_t seed = 0x8B130C2Du;
static uint32_t next_rand(void) {seed = seed*1664525u+1013904223u;return seed;}
static int check(int test) {
    uint32_t n=next_rand();
    int x=(int)(n%1201u)-600;
    int y=(int)((n>>12)%1201u)-600;
    uint32_t flag=(next_rand()>>24)&0xffu;
    private_vm.field5C=(u8)flag;
    D_8015C5CC_15D1CC=commands;
    memset(commands,0xa5,sizeof(commands));
    func_8003EBAC_3F7AC(x,y);
    if (D_8015C5CC_15D1CC!=commands+11){fprintf(stderr,"output pointer at case %d\n",test);return 1;}
    const uint32_t expected_w0[11]={0x06000000u,0xfd100000u,0xf5100000u,0xe6000000u,
        0xf3000000u,0xe7000000u,0xf5101000u,0xf2000000u,0,0xb4000000u,0xb3000000u};
    const uint32_t expected_w1[11]={ (uint32_t)(uintptr_t)&D_800777F0_783F0,
       (uint32_t)(uintptr_t)&D_80076148_76D48,0x07000000u,0,0x077ff100u,0,0,0x0007c0fcu,
       0,((flag&3u)<<9)|((flag&4u)<<23),0x10000400u};
    uint32_t by=(uint32_t)y-2u,bx=(uint32_t)x;
    uint32_t c0=0xe4000000u | ((((bx+15u)<<2)&0xfffu)<<12) | (((by+15u)<<2)&0xfffu);
    uint32_t c1=((((bx<<2)&0xfffu)<<12) | ((by<<2)&0xfffu));
    for(unsigned i=0;i<11;i++){
       uint32_t w0=(i==8?c0:expected_w0[i]),w1=(i==8?c1:expected_w1[i]);
       if (commands[i].w0!=w0||commands[i].w1!=w1){
           fprintf(stderr,"mismatch case %d command %u\n",test,i);return 1;
       }
    }
    if(commands[11].w0!=0xa5a5a5a5u || commands[11].w1!=0xa5a5a5a5u){
       fprintf(stderr,"canary changed\n");return 1;
    }
    return 0;
}
int main(void){for(int i=0;i<4096;i++)if(check(i))return 1; puts("4096 actual-source host cases passed");return 0;}
