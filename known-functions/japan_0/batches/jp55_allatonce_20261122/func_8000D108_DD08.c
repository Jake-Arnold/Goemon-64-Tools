#include "jp_actor_observed.h"
int func_8000D108_DD08(void) {
    int i;
    int mask=0;
    for (i=0;i<3;i++) {
        if(D_8016D430_16E030[i]!=0) mask |= (1<<i);
    }
    return mask;
}
