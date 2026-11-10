/* Research only. Entire object_dispatch.c translation unit, 0x35C64..0x35CC4.
 * Known mismatch at 0x35C9C and 0x35CA0: compiler swaps LUI and RA spill.
 * Do not promote the second function on its standalone match.
 */
typedef signed int s32;
extern s32 D_8016DAB4_16E6B4;
void func_800362DC_36EDC(s32);
void func_80035044_35C44(s32);
void func_800350C4_35CC4(s32);
void func_80035064_35C64(void) {
    func_800362DC_36EDC(D_8016DAB4_16E6B4);
    func_80035044_35C44(D_8016DAB4_16E6B4);
}
void func_80035094_35C94(s32 actor) {
    func_800362DC_36EDC(D_8016DAB4_16E6B4);
    func_800350C4_35CC4(actor);
}
