#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCF34, 52 bytes. */
void func_8000C334_CF34(int idx) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field18 |= 16ULL;
    }
}
