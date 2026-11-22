#include "jp_actor_fields.h"
/* USA original ROM 0xCECC, 64 bytes. */
void func_8000C5A4_D1A4(int idx) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field18 &= ~8ULL;
    }
}
