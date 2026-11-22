/* Execute the actual native-reconstructed C bodies on host, using safe stubs.
   Deliberately choose a task pointer offset +4 so the N64 task+0x5C
   pointer slot is 8-aligned when interpreted by the host's 64-bit ABI. */
#include "common.h"
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
extern void func_801E31A8_59F0B8(void *);
extern void func_801E3244_59F154(void *);
extern void func_801E3278_59F188(void *);
extern void func_801E28D8_59E7E8(void *,u8);
extern void func_801E2B54_59EA64(void *);
f32 D_8020B350_5C7260, D_8020B35C_5C726C, D_8020B360_5C7270, D_8020B364_5C7274;
void *D_8015CCC0_15D8C0;
static void *tracked_task;
static void *tracked_ret;
static unsigned calls;
static unsigned event;
static float observed_x,observed_y,observed_z, observed_float_param;
static u32 observed_flag;
static void *observed_pointer;
static s32 observed_int1,observed_int2;
static int marker, input_marker;
static void reset(void *p) {tracked_task=p;calls=0;event=0;observed_x=observed_y=observed_z=observed_float_param=0;observed_flag=0;observed_pointer=0;observed_int1=0;observed_int2=0;tracked_ret=&marker;}
static int equal_float(float x,float y) { return memcmp(&x,&y,sizeof x)==0; }
static void check_triplet(float expected) { assert(calls==1 && event==3);assert(equal_float(observed_x,expected));assert(equal_float(observed_y,expected));assert(equal_float(observed_z,expected)); }
void func_801E32D4_59F1E4(void *p,float a,float b,float c) {assert(p==tracked_task && calls==0);observed_x=a;observed_y=b;observed_z=c;calls++;event=3;}
void func_801E3834_59F744(void *p,u32 flag) {assert(p==tracked_task && calls==0);observed_flag=flag;float old_a,old_b;memcpy(&old_a,(u8*)p+0xE4,4);memcpy(&old_b,(u8*)p+0xE8,4);assert(old_a==5.0f && old_b==-7.0f);calls++;event=2;}
void func_801DD830_599740(void *p,s32 n) {assert(p==tracked_task && n==4 && calls==0);calls++;event=1;}
void *func_801DB494_5973A4(void *p,void *q,s32 a,s32 b,f32 c) {assert(p==tracked_task && calls==1 && event==1);observed_pointer=q;observed_int1=a;observed_int2=b;observed_float_param=c;calls++;event=2;return tracked_ret;}
static u32 state=0xA751C020u;
static u32 rng(void) {state^=state<<13;state^=state>>17;state^=state<<5;return state;}
static float finite(u32 r) {return (float)((s32)(r%200001u)-100000)/333.0f;}
int main(void) {
 _Alignas(16) u8 raw[512];_Alignas(16) u8 context[512];
 void *task=raw+4; assert(((uintptr_t)task+0x5c)%8==0);
 for(int i=0;i<32768;i++) {
   memset(raw,0,sizeof(raw));memset(context,0,sizeof(context));reset(task);
   D_8020B350_5C7260=finite(rng());func_801E31A8_59F0B8(task);check_triplet(D_8020B350_5C7260);
   reset(task);D_8020B35C_5C726C=finite(rng());func_801E3244_59F154(task);check_triplet(D_8020B35C_5C726C);
   reset(task);D_8020B360_5C7270=(float)(rng()%500000u)/300.0f;D_8020B364_5C7274=finite(rng())/100.0f;
   float ref=(120.0f-D_8020B364_5C7274*sqrtf(D_8020B360_5C7270))/40.0f;
   func_801E3278_59F188(task);check_triplet(ref);
   reset(task);float a=5.0f,b=-7.0f;memcpy((u8*)task+0xE4,&a,4);memcpy((u8*)task+0xE8,&b,4);
   u8 flag=(u8)rng();func_801E28D8_59E7E8(task,flag);assert(calls==1 && event==2 && observed_flag==(u32)flag);
   memcpy(&a,(u8*)task+0xE4,4);memcpy(&b,(u8*)task+0xE8,4);assert(a==0.0f&&b==1.0f);
   reset(task);void *p=context;memcpy((u8*)task+0x5C,&p,sizeof p);D_8015CCC0_15D8C0=&input_marker;
   func_801E2B54_59EA64(task);void *ret=0;memcpy(&ret,context+0x88,sizeof ret);
   assert(calls==2 && event==2 && observed_pointer==D_8015CCC0_15D8C0);
   assert(observed_int1==0x196 && observed_int2==0x80 && observed_float_param==115.0f && ret==&marker);
 }
 puts("GOEMON_FIVE_REAL_C_HOST_SEMANTICS_PASS_32768_ITERS_163840_TOTAL_CALLS");
 return 0;
}
