#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCE24, 36 bytes. */
void func_8000C224_CE24(int idx, int value) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field24 = value;
    }
}
