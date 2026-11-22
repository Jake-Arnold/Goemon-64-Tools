#include "jp_actor_fields.h"
/* USA original ROM 0xCF34, 52 bytes. */
void func_8000C60C_D20C(int idx) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field18 |= 16ULL;
    }
}
