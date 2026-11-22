#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCF68, 64 bytes. */
void func_8000C368_CF68(int idx) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field18 &= ~16ULL;
    }
}
