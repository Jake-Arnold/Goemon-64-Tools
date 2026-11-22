#include "jp_actor_fields.h"
/* USA original ROM 0xCDE4, 64 bytes. */
void func_8000C4FC_D0FC(int idx) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field18 &= ~4ULL;
    }
}
