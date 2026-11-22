#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCDB0, 52 bytes. */
void func_8000C1B0_CDB0(int idx) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field18 |= 4ULL;
    }
}
