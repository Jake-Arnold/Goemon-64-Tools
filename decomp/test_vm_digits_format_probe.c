/* Synthetic host-only behaviour of research digit-formatting candidate.
 * Does not compare original MIPS instructions or execute the game.
 */
#include <stdint.h>
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define VM_DIGITS_HOST_TEST 1
#include "candidates/vm_digits_format_probe.c"
char D_801C7780_1C8380[64];
const char D_8007CF60_7DB60[] = "%d";
s32 D_801C7740_1C8340;
char *D_801C779C_1C839C;
s16 D_801C77A8_1C83A8[64];
s16 *D_801C77DC_1C83DC;
s32 D_801C7754_1C8354;
static int callbacks;
static s32 callback_arg;
void func_8003EB34_3F734(s32 x) { callbacks++; callback_arg = x; }
static void check(s32 x, unsigned case_num) {
    char expected[64];
    size_t n;
    int printed = snprintf(expected, sizeof(expected), "%d", x);
    if (printed < 1 || (size_t)printed >= sizeof(expected)) abort();
    n = (size_t)printed;
    memset(D_801C7780_1C8380, 0x69, sizeof D_801C7780_1C8380);
    for (unsigned j = 0; j < 64; j++) D_801C77A8_1C83A8[j] = (s16)0x5A5A;
    D_801C779C_1C839C = NULL;
    D_801C77DC_1C83DC = NULL;
    D_801C7740_1C8340 = x;
    D_801C7754_1C8354 = (s32)case_num;
    callbacks = 0;
    func_8003F480_40080();
    assert(callbacks == 1 && callback_arg == (s32)case_num);
    assert(strcmp(D_801C7780_1C8380, expected) == 0);
    assert(D_801C779C_1C839C == D_801C7780_1C8380 + n);
    assert(D_801C77DC_1C83DC == D_801C77A8_1C83A8 + n);
    for(size_t j=0;j<n;j++) assert(D_801C77A8_1C83A8[j] == (s16)((unsigned char)expected[j]-0x30));
    assert(D_801C77A8_1C83A8[n] == -1);
    assert(D_801C77A8_1C83A8[n+1] == (s16)0x5A5A);
}
int main(void) {
    const s32 boundaries[] = {0,1,9,10,99,100,999,1000,123456789,INT_MAX,INT_MIN,-1,-9,-10,-99,-100,-999,-1000};
    unsigned state=0xA52F9D13u;
    unsigned n=0;
    for (size_t i=0;i<sizeof(boundaries)/sizeof(boundaries[0]);i++) check(boundaries[i],++n);
    while (n<1000) {
        state^=state<<13;state^=state>>17;state^=state<<5;
        check((s32)state,++n);
    }
    puts("VM digits host: 1000/1000 deterministic cases passed");
    return 0;
}
