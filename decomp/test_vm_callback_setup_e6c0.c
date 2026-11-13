/* Host model only: mock callbacks and typed VM data, not original MIPS. */
#include <stddef.h>
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define GOEMON_VM_E6C0_HOST_TEST 1
#include "candidates/vm_callback_setup_e6c0.c"

void *D_801C78D0_1C84D0;
s32 D_801C7754_1C8354;
void *D_80167C48_168848[4];
VmChoice *vm_e6c0_choice_base;
u8 D_801C77F4_1C83F4[20*16];
u8 D_801C781C_1C841C[20*16];
s32 D_801C77E0_1C83E0;
static VmWindow windows[4];
static u32 choice_storage[2+5*16];
static u32 script_words[4*16+1];
static unsigned callbacks, resources, expected_records;
static s32 expected_window;
static unsigned early_has_callback;
static unsigned saw_callback_taken, saw_callback_skipped;
static unsigned saw_empty_stream, saw_nonempty_stream;
static unsigned saw_single_record_exit, saw_loop_continue;
_Static_assert(offsetof(VmWindow, x)==0x32,"window x");
_Static_assert(offsetof(VmWindow, y)==0x34,"window y");
_Static_assert(offsetof(VmWindow, addx)==0x50,"window addx");
_Static_assert(offsetof(VmWindow, addy)==0x54,"window addy");
_Static_assert(offsetof(VmWindow, offx)==0x6e,"window offx");
_Static_assert(offsetof(VmWindow, offy)==0x74,"window offy");
_Static_assert(sizeof(VmChoice)==20,"VM choice is 20 bytes");

s32 func_80034B24_35724(void *handler,s32 arg) {
  assert(callbacks++ == 0 && handler==D_801C78D0_1C84D0 && arg==0);
  D_801C7754_1C8354=expected_window;
  return 0;
}
s32 func_8003DE48_3EA48(s32 source) {
  assert((u32)source == script_words[resources*4+1]);
  assert(resources < expected_records);
  resources++;
  D_801C7754_1C8354 = (s32)(resources%3+1); /* Global may change during callback. */
  return (s32)((u32)source ^ 0x539AB123u);
}
void func_8003EB34_3F734(s32 idx,s16 *output) {
  assert(idx==D_801C7754_1C8354);
  assert(idx==(s32)(resources%3+1));
  assert((u32)(uintptr_t)output==(script_words[(resources-1)*4+1] ^ 0x539AB123u));
  callbacks++;
}
void func_8003E9E8_3F5E8(VmChoice *p){
  assert(p==vm_e6c0_choice_base);
  assert(resources==expected_records);
  assert(D_801C77E0_1C83E0==-33);
  callbacks++;
}
static u32 next(u32 *state) {u32 x=*state;x^=x<<13;x^=x>>17;x^=x<<5;*state=x;return x;}
static void check(u32 *seed,unsigned ncase) {
  expected_records=next(seed)%12;
  expected_window=(s32)(1+(next(seed)%3));
  early_has_callback=(next(seed)&1);
  if(early_has_callback)saw_callback_taken++;else saw_callback_skipped++;
  if(expected_records==0)saw_empty_stream++;else saw_nonempty_stream++;
  if(expected_records==1)saw_single_record_exit++;
  if(expected_records>1)saw_loop_continue++;
  D_801C7754_1C8354=early_has_callback ? 0 : expected_window;
  D_801C78D0_1C84D0=early_has_callback ? (void *)&script_words[16] : 0;
  for(int j=0;j<4;j++){
    VmWindow *w=&windows[j];
    memset(w,0,sizeof(*w));
    w->x=(s16)next(seed);w->y=(s16)next(seed);
    w->offx=(s16)next(seed);w->offy=(s16)next(seed);
    w->addx=(s32)next(seed);w->addy=(s32)next(seed);
    D_80167C48_168848[j]=w;
  }
  for(unsigned j=0;j<expected_records;j++){
    script_words[4*j]=(next(seed)&0xFFFFu) | 0x10000u;
    script_words[4*j+1]=next(seed);
    script_words[4*j+2]=next(seed);
    script_words[4*j+3]=next(seed);
  }
  script_words[4*expected_records]=0x8012;
  for(unsigned j=4*expected_records+1;j<sizeof(script_words)/sizeof(script_words[0]);j++)script_words[j]=0x12345;
  for(unsigned i=0;i<sizeof(choice_storage)/sizeof(choice_storage[0]);i++)choice_storage[i]=0xDEADBEEFu;
  vm_e6c0_choice_base=(VmChoice *)(choice_storage+2);
  D_801C77E0_1C83E0=-33;
  callbacks=resources=0;
  u32 *result=func_8003E6C0_3F2C0(script_words);
  assert(result==script_words+4*expected_records);
  assert(D_801C77E0_1C83E0==2);
  assert(resources==expected_records);
  assert(callbacks==resources + 1 + early_has_callback);
  VmWindow *w=windows+expected_window;
  for(unsigned j=0;j<expected_records;j++){
     VmChoice *p=vm_e6c0_choice_base+j;
     assert(p->x==(u32)((u32)(s32)w->x+(u32)(s32)w->offx+(u32)w->addx));
     assert(p->y==(u32)((u32)(s32)w->y+(u32)(s32)w->offy+(u32)w->addy));
     if(j==0)assert(p->previous==0);
     else assert(p->previous==(u32)(uintptr_t)(D_801C77F4_1C83F4+20*j));
     if(j+1<expected_records)assert(p->next==(u32)(uintptr_t)(D_801C781C_1C841C+20*j));
     else assert(p->next==0);
     assert(p->script==(u32)(uintptr_t)(script_words+4*j+2));
  }
  assert(vm_e6c0_choice_base[0].previous==0);
  if(expected_records==0) assert(choice_storage[0]==0);
  assert(choice_storage[1]==0xDEADBEEFu);
  assert(choice_storage[2+5*expected_records]==0xDEADBEEFu);
  (void)ncase;
}
int main(void){
  u32 seed=0x6C023F2Cu;
  for(unsigned i=0;i<400;i++)check(&seed,i);
  assert(saw_callback_taken&&saw_callback_skipped);
  assert(saw_empty_stream&&saw_nonempty_stream);
  assert(saw_single_record_exit&&saw_loop_continue);
  puts("VM callback E6C0: 400/400 synthetic host scenarios passed; all callback/loop branches covered");
  return 0;
}
