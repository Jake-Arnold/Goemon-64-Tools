#include "jp_actor_fields.h"
/* USA original ROM 0xCF68, 64 bytes. */
void func_8000C640_D240(int idx) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field18 &= ~16ULL;
    }
}
