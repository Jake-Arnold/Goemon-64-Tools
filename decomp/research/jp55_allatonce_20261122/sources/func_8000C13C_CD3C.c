#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCD3C, 52 bytes. */
void func_8000C13C_CD3C(int idx) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field18 |= 2ULL;
    }
}
