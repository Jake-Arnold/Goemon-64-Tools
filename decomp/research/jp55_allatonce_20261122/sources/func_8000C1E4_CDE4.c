#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCDE4, 64 bytes. */
void func_8000C1E4_CDE4(int idx) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field18 &= ~4ULL;
    }
}
