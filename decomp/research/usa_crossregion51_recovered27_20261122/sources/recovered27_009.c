#include "jp_actor_observed.h"
int func_8000D3B8_DFB8(void) {
    int i;
    int mask=0;
    for (i=0;i<3;i++) {
        if(D_80167C48_168848[i]!=0) mask |= (1<<i);
    }
    return mask;
}
