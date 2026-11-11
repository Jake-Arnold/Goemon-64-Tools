#include <assert.h>
#include "common.h"

u32 D_800573D8_57FD8[4] = {0, 0x80000000u, 0xF1234567u, 0x7FFFFFFFu};
u32 func_80001D94_2994(u16);

int main(void) {
    assert(func_80001D94_2994(0) == 0);
    assert(func_80001D94_2994(1) == 0);
    assert(func_80001D94_2994(2) == 0x71234567u);
    assert(func_80001D94_2994(3) == 0x7FFFFFFFu);
    assert(D_800573D8_57FD8[2] == 0xF1234567u);
    return 0;
}
