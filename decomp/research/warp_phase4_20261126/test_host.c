/* Synthetic host checks only. Source reads a byte via character alias, so seed
 * the local word's object representation directly (no host-endian conversion). */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#ifdef JP
#include "sources/japan_0_scalar.c"
#define SYSTEM g_system_ptr
#define OBJ D_8020151C_5BD4EC
#define PLAYER D_80201510_5BD4E0
#define CHECK func_8021A28C_5D581C
#define EFFECT func_80200180_5BC150
#define DECODE func_8021A0C0_5D5650
#define NEXT func_8021A280_5D5810
#define REGISTER func_80034E8C_35A8C
#define DISPATCH func_80219FC0_5D5550
#else
#include "sources/usa_scalar.c"
#define SYSTEM D_8015C5C8_15D1C8
#define OBJ D_801FC60C_5B851C
#define PLAYER D_801FC600_5B8510
#define CHECK func_802154FC_5D09CC
#define EFFECT func_801FB270_5B7180
#define DECODE func_80215330_5D0800
#define NEXT func_802154F0_5D09C0
#define REGISTER func_8003521C_35E1C
#define DISPATCH func_80215230_5D0700
#endif
#define KIND 0xcf898
#define LOCK 0x3ae29
#define STORE 0xcf894
/* 0xcf894 is 4 mod 8. Choose a host base that aligns the pointer store. */
static _Alignas(8) u8 bank1[0xd0000+8],bank2[0xd0000+8];
static u8 *s1=bank1+4,*s2=bank2+4;
u8 *SYSTEM;
void *OBJ;
Player *PLAYER;
static Player player;
static Task task;
static int object1,object2,collision_object;
static int answer,mutate,order,ncalls,expect_mask;
int CHECK(void *a,void *b,u8 mask){assert(order==0);assert(a==&object1&&b==&collision_object&&mask==expect_mask);order=1;ncalls++;return answer;}
void EFFECT(void){assert(order==1&&player.flags==0x1204);order=2;ncalls++;if(mutate){SYSTEM=s2;OBJ=&object2;}}
void DECODE(Task *t){assert(t==&task);assert(order==0||order==2);if(order==2){void *v;memcpy(&v,SYSTEM+STORE,sizeof v);assert(v==OBJ);}order=3;ncalls++;}
void NEXT(void){assert(0&&"callback registered, not invoked");}
void REGISTER(void (*f)(void)){assert(order==3&&f==NEXT);order=4;ncalls++;}
int main(void){unsigned k,b,locked,present,hit;unsigned cases=0;void *nil=0;PLAYER=&player;
 /* On a 64-bit host the original adjacent 4-byte pointer and kind byte overlap
  * in memory. No source read of kind occurs after the pointer store. Reset both
  * fields for each case. */
 for(k=0;k<256;k++)for(b=0;b<256;b+=17)for(locked=0;locked<2;locked++)for(present=0;present<2;present++)for(hit=0;hit<2;hit++){
  SYSTEM=s1;OBJ=present?&object1:0;player.flags=0x1200;memcpy(s1+STORE,&nil,sizeof nil);memcpy(s2+STORE,&nil,sizeof nil);s1[KIND]=k;s1[LOCK]=locked;task.exit.b[2]=(signed char)b;answer=hit?0x7fff:0;mutate=hit;order=ncalls=0;expect_mask=b&0xf0;
  DISPATCH(&task,&collision_object);
  if(!k||locked|| (k>=17&&!present))assert(order==0&&ncalls==0&&player.flags==0x1200);
  else if(k>=17){if(hit)assert(order==4&&ncalls==4&&player.flags==0x1204&&SYSTEM==s2&&OBJ==&object2);else assert(order==1&&ncalls==1&&player.flags==0x1200);}
  else if((b&15)==k)assert(order==4&&ncalls==2&&player.flags==0x1200);
  else assert(order==0&&ncalls==0&&player.flags==0x1200);
  cases++;
 }
 printf("%u synthetic dispatcher cases PASS\n",cases);return 0;
}
