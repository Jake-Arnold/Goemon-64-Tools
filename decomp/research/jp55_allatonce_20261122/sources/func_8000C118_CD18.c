#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCD18, 36 bytes. */
void func_8000C118_CD18(int idx, int value) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field70 = value;
    }
}
