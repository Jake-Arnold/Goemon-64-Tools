/* Native Japanese rev-0 matching C: bit-array operations.
 * Original ROM 0x16DF0..0x16E70, VMA 0x800161F0..0x80016270.
 * Shared semantics with verified USA decomp/bit_array.c; original Japanese
 * IDO 5.3 -O2 -mips2 machine code and the full linked ROM were verified.
 */
typedef unsigned char u8;

void func_800161F0_16DF0(int base, int bit) {
    u8 *p = (bit >> 3) + base;
    *p |= 1 << (bit & 7);
}

void func_80016214_16E14(int base, int bit) {
    u8 *p = (bit >> 3) + base;
    *p &= ~(1 << (bit & 7));
}

int func_8001623C_16E3C(int base, int bit) {
    u8 *p = (bit >> 3) + base;
    int result = 0;
    if (*p & (1 << (bit & 7))) { result = 1; }
    else { result = 0; }
    return result;
}
