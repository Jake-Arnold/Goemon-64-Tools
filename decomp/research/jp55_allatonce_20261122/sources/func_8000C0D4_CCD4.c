#include "jp_actor_observed.h"
void func_8000C0D4_CCD4(int i) {
 Actor *p = D_8016D430_16E030[i];
 if(p) {
   p->field6e = 0;
   p->field74 += p->field76;
   p->field6c = 0;
   p->field72++;
 }
}
