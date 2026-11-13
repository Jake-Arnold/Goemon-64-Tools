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
  D_8015C5CC_15D1CC = NULL;
  D_80077860_78460 = owner;
}

static void check_zero_case(void) {
  u32 memory[32];
  u32 expect[22];

  for (unsigned j = 0; j < 32; j++) memory[j] = 0xC0DE0000U + j;
  D_8015C5CC_15D1CC = memory + 8;
  D_801C78D8_1C84D8 = 0;
  D_801C78DC_1C84DC = 0;
  D_80077860_78460 = owner;
  memset(owner, 0, sizeof(owner));

  expect[0] = 0x06000000; expect[1] = VM_ADDR(D_800777F0_783F0);
  expect[2] = 0xFD100000; expect[3] = VM_ADDR(D_80077150_77D50);
  expect[4] = 0xF5100000; expect[5] = 0x07000000;
  expect[6] = 0xE6000000; expect[7] = 0;
  expect[8] = 0xF3000000; expect[9] = 0x071FF100;
  expect[10] = 0xE7000000; expect[11] = 0;
  expect[12] = 0xF5101000; expect[13] = 0;
  expect[14] = 0xF2000000; expect[15] = 0x0007C03C;
  expect[16] = 0xE403C03C; expect[17] = 0;
  expect[18] = 0xB4000000; expect[19] = 0;
  expect[20] = 0xB3000000; expect[21] = 0x10000400;

  func_8003E234_3EE34();

  assert(D_8015C5CC_15D1CC == memory + 30);
  for (unsigned j = 0; j < 8; j++) assert(memory[j] == 0xC0DE0000U + j);
  assert(memory[30] == 0xC0DE001EU && memory[31] == 0xC0DE001FU);
  assert(memory[8] == 0x06000000);
  assert(memory[29] == 0x10000400);
  for (unsigned j = 0; j < 22; j++) {
    if (memory[j + 8] != expect[j]) {
      fprintf(stderr, "zero case command word %u: %08X expected %08X\n",
              j, memory[j + 8], expect[j]);
      abort();
    }
  }
  D_8015C5CC_15D1CC = NULL;
  D_80077860_78460 = owner;
}

static void check_owner_byte_alias(void) {
  u32 memory[32];
  u32 expect[22];
  u32 x = 5;
  u32 y = 9;
  u8 *alias_owner;

  for (unsigned j = 0; j < 32; j++) memory[j] = 0xC0DE0000U + j;
  D_8015C5CC_15D1CC = memory + 8;
  D_801C78D8_1C84D8 = x;
  D_801C78DC_1C84DC = y;
  alias_owner = (u8 *)memory + 26 * sizeof(u32) - 0x5D;
  D_80077860_78460 = alias_owner;
  alias_owner[0x5D] = 1;
  assert(alias_owner[0x5D] == 1);

  expect[0] = 0x06000000; expect[1] = VM_ADDR(D_800777F0_783F0);
  expect[2] = 0xFD100000; expect[3] = VM_ADDR(D_80077150_77D50);
  expect[4] = 0xF5100000; expect[5] = 0x07000000;
  expect[6] = 0xE6000000; expect[7] = 0;
  expect[8] = 0xF3000000; expect[9] = 0x071FF100;
  expect[10] = 0xE7000000; expect[11] = 0;
  expect[12] = 0xF5101000; expect[13] = 0;
  expect[14] = 0xF2000000; expect[15] = 0x0007C03C;
  expect[16] = 0xE4000000 | (((((x + 15) * 4) & 0xFFF) << 12)) |
               (((y + 15) * 4) & 0xFFF);
  expect[17] = (((x * 4) & 0xFFF) << 12) | ((y * 4) & 0xFFF);
  expect[18] = 0xB4000000;
  expect[19] = 0; /* B400 w0 overwrites the aliased odd owner byte first. */
  expect[20] = 0xB3000000; expect[21] = 0x10000400;

  func_8003E234_3EE34();

  assert(D_8015C5CC_15D1CC == memory + 30);
  for (unsigned j = 0; j < 8; j++) assert(memory[j] == 0xC0DE0000U + j);
  assert(memory[30] == 0xC0DE001EU && memory[31] == 0xC0DE001FU);
  assert(memory[8] == 0x06000000);
  assert(memory[29] == 0x10000400);
  assert(memory[26] == 0xB4000000);
  assert(memory[27] == 0);
  assert((alias_owner[0x5D] & 1) == 0);
  for (unsigned j = 0; j < 22; j++) {
    if (memory[j + 8] != expect[j]) {
      fprintf(stderr, "alias case command word %u: %08X expected %08X\n",
              j, memory[j + 8], expect[j]);
      abort();
    }
  }
  D_8015C5CC_15D1CC = NULL;
  D_80077860_78460 = owner;
}

int main(void) {
  unsigned seed = 0xCE11AB1E;
  for (unsigned i = 0; i < 1000; i++) check(i, &seed);
  check_zero_case();
  check_owner_byte_alias();
  puts("VM graphics writer: 1000 synthetic cases plus zero and owner-alias cases passed");
  return 0;
}
