/* Host-only mock display-list regression; not original-MIPS emulation. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#define GOEMON_VM_DISPLAY_HOST_TEST 1
#ifndef GOEMON_VM_DISPLAY_SOURCE
#define GOEMON_VM_DISPLAY_SOURCE "candidates/vm_display_e234.c"
#endif
#include GOEMON_VM_DISPLAY_SOURCE

#ifdef GOEMON_VM_DISPLAY_VOLATILE
u32 *volatile D_8015C5CC_15D1CC;
#else
u32 *D_8015C5CC_15D1CC;
#endif
u8 D_800777F0_783F0[16];
u8 D_80077150_77D50[16];
u8 D_80076148_76D48[16];
u32 D_801C78D8_1C84D8, D_801C78DC_1C84DC;
u8 owner[0x60];u8 *D_80077860_78460=owner;
static u32 randword(unsigned *state){unsigned x=*state;x^=x<<13;x^=x>>17;x^=x<<5;*state=x;return x;}
static void check(unsigned idx, unsigned *seed){
  u32 memory[26];
  u32 expect[22];
  for (unsigned j=0;j<26;j++) memory[j]=0xC0DE0000+j;
  D_8015C5CC_15D1CC=memory+2;
  D_801C78D8_1C84D8=randword(seed);
  D_801C78DC_1C84DC=randword(seed);
  owner[0x5C]=(u8)(randword(seed));owner[0x5D]=(u8)(randword(seed));
  u32 a=D_801C78D8_1C84D8,b=D_801C78DC_1C84DC;
#ifdef GOEMON_VM_DISPLAY_SECOND
  a=randword(seed);b=randword(seed);
#endif
  expect[0]=0x06000000; expect[1]=VM_ADDR(D_800777F0_783F0);
  expect[2]=0xFD100000;
#ifdef GOEMON_VM_DISPLAY_SECOND
  expect[3]=VM_ADDR(D_80076148_76D48);
#else
  expect[3]=VM_ADDR(D_80077150_77D50);
#endif
  expect[4]=0xF5100000; expect[5]=0x07000000;
  expect[6]=0xE6000000; expect[7]=0;
  expect[8]=0xF3000000;
#ifdef GOEMON_VM_DISPLAY_SECOND
  expect[9]=0x077FF100;
#else
  expect[9]=0x071FF100;
#endif
  expect[10]=0xE7000000;expect[11]=0;
  expect[12]=0xF5101000;expect[13]=0;
  expect[14]=0xF2000000;
#ifdef GOEMON_VM_DISPLAY_SECOND
  expect[15]=0x0007C0FC;
#else
  expect[15]=0x0007C03C;
#endif
#ifdef GOEMON_VM_DISPLAY_SECOND
  u32 by=b-2;
#else
  u32 by=b;
#endif
  expect[16]=0xE4000000 | (((((a+15)*4)&0xfff)<<12)) | ((((by+15)*4)&0xfff));
  expect[17]=(((((a*4)&0xfff)<<12))) | (((by*4)&0xfff));
  expect[18]=0xB4000000;
#ifdef GOEMON_VM_DISPLAY_SECOND
  expect[19]=((owner[0x5C]&3)<<9)|((owner[0x5C]&4)<<23);
#else
  expect[19]=((owner[0x5D]&1)<<25);
#endif
  expect[20]=0xB3000000;expect[21]=0x10000400;
#ifdef GOEMON_VM_DISPLAY_SECOND
  func_8003EBAC_3F7AC(a,b);
#else
  func_8003E234_3EE34();
#endif
  assert(D_8015C5CC_15D1CC == memory+24);
  assert(memory[0]==0xC0DE0000 && memory[1]==0xC0DE0001);
  assert(memory[24]==0xC0DE0018 && memory[25]==0xC0DE0019);
  for(unsigned j=0;j<22;j++) {
     if(memory[j+2]!=expect[j]) {fprintf(stderr,"case %u command word %u: %08X expected %08X\n",idx,j,memory[j+2],expect[j]);abort();}
  }
}
int main(void){ unsigned seed=0xCE11AB1E;for(unsigned i=0;i<1000;i++)check(i,&seed);puts("VM graphics writer: 1000/1000 synthetic host cases passed");return 0;}
