/* Isolated MIPS matching candidate, not included in the verified manifest.
 * Original USA entry 0x8003F350, ROM offset 0x3FF50, extent 44 bytes.
 * The full VM unit uses a callback-pointer type for the first argument;
 * s32 here models the 32-bit MIPS ABI without importing unrelated headers.
 */
typedef signed int s32;
extern s32 D_801C7740_1C8340;
extern s32 D_801C7750_1C8350;
extern s32 func_80034B24_35724(s32 callback, s32 flags);

void func_8003F350_3FF50(void) {
    D_801C7750_1C8350 = func_80034B24_35724(D_801C7740_1C8340, 0);
}
