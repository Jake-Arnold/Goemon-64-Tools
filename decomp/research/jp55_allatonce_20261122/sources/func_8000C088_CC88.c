#include "jp_actor_observed.h"
void func_8000C088_CC88(int i) {
 Actor *p = D_8016D430_16E030[i];
 if (p && p->field30 == 4) {
   p->field30 = 5;
   p->field10 |= 1ULL;
 }
}
