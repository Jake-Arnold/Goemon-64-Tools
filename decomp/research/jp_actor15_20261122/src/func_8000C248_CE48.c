#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xCE48, 40 bytes. */
void func_8000C248_CE48(int idx, float value) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field80 = value;
    }
}
