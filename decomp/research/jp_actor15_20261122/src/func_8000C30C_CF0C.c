#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCF0C, 40 bytes. */
void func_8000C30C_CF0C(int idx, float value) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field88 = value;
    }
}
