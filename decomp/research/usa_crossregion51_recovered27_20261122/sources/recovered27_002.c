#include "jp_actor_fields.h"
/* USA original ROM 0xCDB0, 52 bytes. */
void func_8000C4C8_D0C8(int idx) {
    JPActorObserved *p = D_80167C48_168848[idx];
    if (p != 0) {
        p->field18 |= 4ULL;
    }
}
