#include "jp_actor_fields.h"
/* USA original ROM 0xD200, 52 bytes. */
void func_8000C8D0_D4D0(int idx, int a, int b, int c, int d) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field64 = a; p->field66 = b; p->field68 = c; p->field6A = d;
    }
}
