#include "jp_actor_observed.h"
int func_8000BFFC_CBFC(int i) {
 Actor *p=D_8016D430_16E030[i];
 if(p) {
 i=p->field30;
 if(i==1)return 1;
 if(i==2)return 1;
 if(i==3)return 1;
 if(i==5)return 2;
 if(i==6)return 2;
 }
 return 0;
}
