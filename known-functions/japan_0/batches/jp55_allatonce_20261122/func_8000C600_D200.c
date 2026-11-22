#include "jp_actor_fields.h"
/* Japan rev-0 original ROM 0xD200, 52 bytes. */
void func_8000C600_D200(int idx, int a, int b, int c, int d) {
    JPActorObserved *p = D_8016D430_16E030[idx];
    if (p != 0) {
        p->field64 = a; p->field66 = b; p->field68 = c; p->field6A = d;
    }
}
