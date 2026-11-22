#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCFA8, 40 bytes. */
void func_8000C3A8_CFA8(int idx, float value) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field44 = value;
    }
}
