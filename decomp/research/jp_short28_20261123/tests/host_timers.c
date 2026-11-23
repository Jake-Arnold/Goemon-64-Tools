#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/* Host ABI models the 0xD4 original timer field, without claiming LP64 ABI equivalence. */
typedef struct { unsigned char pad[0xD4]; int32_t timer; } Actor;
_Static_assert(offsetof(Actor,timer)==0xD4, "original timer offset");
static int call0,call1,call2;
void func_802060A8_630B28(void* p){ (void)p; call0++; }
void func_801F74A8_621F28(void* p){ (void)p; call1++; }
void func_801F75C4_622044(void* p){ (void)p; call2++; }
extern void func_80206078_630AF8(Actor*);
extern void func_801F72A8_621D28(Actor*);
extern void func_801F72D8_621D58(Actor*);
int main(void){
  Actor a;int count=0;
  for (int which=0;which<3;which++) {
    for(int i=0;i<4096;i++) {
      memset(&a,0,sizeof(a));
      int32_t original=(int32_t)(i%1025)-500;
      a.timer=original;
      int prev=which==0?call0:which==1?call1:call2;
      if(which==0)func_80206078_630AF8(&a);
      if(which==1)func_801F72A8_621D28(&a);
      if(which==2)func_801F72D8_621D58(&a);
      int now=which==0?call0:which==1?call1:call2;
      if(a.timer!=original-1 || now-prev!=(original-1<=0))return 3;
      count++;
    }
  }
  if(count!=12288)return 4;
  printf("JP_SHORT28_TIMER_HOST_12288_PASS\n");
  return 0;
}
