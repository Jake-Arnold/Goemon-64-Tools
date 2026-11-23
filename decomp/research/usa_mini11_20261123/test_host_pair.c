/* Host-sanitizer semantic regression of the two actual Mini native C bodies. */
#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned char u8;
typedef float f32;
extern void func_801E28D8_59E7E8(void *,u8);
extern void func_801E3278_59F188(void *);
f32 D_8020B350_5C7260,D_8020B35C_5C726C,D_8020B360_5C7270,D_8020B364_5C7274;
static unsigned calls=0,flag;
static float observed[3];
static void *target;
void func_801E3834_59F744(void *p,unsigned v){assert(p==target && calls==0);flag=v;calls++;}
void func_801E32D4_59F1E4(void *p,float a,float b,float c){assert(p==target && calls==0);observed[0]=a;observed[1]=b;observed[2]=c;calls++;}
static uint32_t seed=0x761acfe2u;
static uint32_t random32(void){seed^=seed<<13;seed^=seed>>17;seed^=seed<<5;return seed;}
static int same_float(f32 a,f32 b){return memcmp(&a,&b,sizeof(a))==0;}
int main(void){
  _Alignas(16) unsigned char buf[512];target=buf;
  for(unsigned i=0;i<32768;i++){
    memset(buf,0x55,sizeof(buf));
    D_8020B360_5C7270=(f32)(random32()%5000000)/1000.0f;
    D_8020B364_5C7274=(f32)((int)(random32()%200000u)-100000)/1000.0f;
    f32 expected=(120.0f-D_8020B364_5C7274*sqrtf(D_8020B360_5C7270))/40.0f;
    calls=0;func_801E3278_59F188(target);
    assert(calls==1);
    for(int j=0;j<3;j++)assert(same_float(observed[j],expected));
    f32 olda=5.0f,oldb=-7.0f,got;
    memcpy(buf+0xe4,&olda,4);memcpy(buf+0xe8,&oldb,4);
    calls=0;u8 arg=(u8)random32();func_801E28D8_59E7E8(target,arg);
    assert(calls==1 && flag==(unsigned)arg);
    memcpy(&got,buf+0xe4,4);assert(same_float(got,0.0f));
    memcpy(&got,buf+0xe8,4);assert(same_float(got,1.0f));
  }
  puts("USA_MINI_ACTUAL_PAIR_ASAN_UBSAN_32768_PASS");return 0;
}
