#include "goemon_watch.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static uint8_t mem[0x800000];
static int rdr(void *x, uint32_t address, void *output, uint32_t n) {
    (void)x;
    uint32_t off=address&0x1fffffffu;
    if(off+n>sizeof(mem))return -1;
    memcpy(output,mem+off,n);
    return 0;
}
static void put32(uint32_t a,uint32_t v){a &= 0x1fffffffu;mem[a]=v>>24;mem[a+1]=v>>16;mem[a+2]=v>>8;mem[a+3]=v;}
int main(void){
    GoemonCheckpointIO io={0,rdr,0}; GoemonWatch w;
    put32(0x8015C5DC,1);put32(0x8015C5E0,10);put32(0x8015C5E4,8);
    put32(0x8015C5E8,100);put32(0x8015C5EC,2);
    mem[0x0C7AB2]=1;mem[0x0C7AB3]=0xD1;mem[0x15C6BF]=1;
    if(goemon_watch_read(&io,&w))return 1;
    if(w.character!=1 || w.map_id!=0x1D1 || w.ryo!=100 || w.optional_items[0]!=1 || w.warnings)return 2;
    put32(0x8015C5E8,10000);
    if(goemon_watch_read(&io,&w) || !(w.warnings&4))return 3;
    puts("portable native watch tests passed");
    return 0;
}
