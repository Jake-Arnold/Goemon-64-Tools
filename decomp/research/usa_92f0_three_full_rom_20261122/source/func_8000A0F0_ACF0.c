#include "common.h"

/* Five calls in their original order. All target functions remain assembly-owned. */
void func_8000A130_AD30(void);
void func_8000A4F8_B0F8(void);
void func_8000A344_AF44(void);
void func_8000A430_B030(void);
void func_8000A614_B214(void);

void func_8000A0F0_ACF0(void) {
    func_8000A130_AD30();
    func_8000A4F8_B0F8();
    func_8000A344_AF44();
    func_8000A430_B030();
    func_8000A614_B214();
}
