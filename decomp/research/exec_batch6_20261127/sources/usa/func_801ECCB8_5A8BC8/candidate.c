#include "m2c_types.h"
void *func_801E8F50_5A4E60(void *, u8); /* extern */
void func_801ED1F0_5A9100(void *); /* extern */

void func_801ECCB8_5A8BC8(void *arg0, u8 arg1) {
    void *temp_v0;

    temp_v0 = func_801E8F50_5A4E60(arg0, arg1);
    if (temp_v0 != NULL) {
        func_801ED1F0_5A9100(temp_v0);
    }
}
