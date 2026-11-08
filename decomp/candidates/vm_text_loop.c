/* Research-only USA 0x8003DBEC / ROM 0x3E7EC VM text-loop candidate.
 * IDO 5.3 -O2 -mips2 -G 0 -non_shared produces a 472-byte function symbol,
 * equal in SIZE to the original but NOT verified instruction-byte equivalent.
 * Not integrated into script_vm.c, the manifest, or results inventories.
 * The halfword at +0xA is a member of global VmWork at 0x801C77E8;
 * it is NOT a field of the separate script pointer stored at offset zero.
 * An immediate retry bypasses the outer iteration bound/count update.
 * This standalone declaration is for isolated codegen/host test only.
 */
typedef signed int s32;
typedef unsigned int u32;
typedef unsigned short u16;
typedef struct {
    s32 script_word; /* +0x0, pointer-sized game address returned from step */
    u16 unk4, unk6;
    short marker;
    u16 gate_halfword; /* +0xA, within the global VmWork, not script pointee */
    s32 choice_state;
    s32 countdown;
} VmWork;
typedef struct {u16 status, held, pressed;} Controller;
extern VmWork D_801C77E8_1C83E8;
extern s32 D_801C77D8_1C83D8;
extern s32 D_801C7754_1C8354;
extern s32 D_801C77E0_1C83E0;
extern s32 D_801C7770_1C8370;
extern s32 D_801C7774_1C8374;
extern s32 D_80077858_78458;
extern Controller D_801C7908_1C8508;
extern s32 func_8003DE80_3EA80(s32, s32);
extern s32 func_8003DE48_3EA48(s32);
extern void func_8003E680_3F280(void);
void func_8003DBEC_3E7EC(void) {
    VmWork *work = &D_801C77E8_1C83E8;
    s32 retry_count = 0;
    s32 outer_count = 0;
    if (D_801C77D8_1C83D8 <= 0) return;
    for (;;) {
        s32 state;
retry:
        D_801C77E8_1C83E8.script_word = func_8003DE80_3EA80(D_801C7754_1C8354, work->script_word);
        state = D_801C77E0_1C83E0;
        if (state == 3 || state == 4 || state == 5 || state == 6) {
            D_801C77E8_1C83E8.gate_halfword = 0;
            break;
        }
        D_801C77E0_1C83E0 = 1;
        if (D_801C77E8_1C83E8.script_word == 0) {
            D_801C77E8_1C83E8.script_word = 0;
            D_801C77E0_1C83E0 = 0;
            break;
        }
        if (D_801C7770_1C8370 == 0) {
            if (D_801C7908_1C8508.pressed & 0x4000) {
                D_801C77E8_1C83E8.gate_halfword = 0;
                if (D_801C7774_1C8374 == 0) {
                    func_8003E680_3F280();
                    return;
                }
                D_801C77E0_1C83E0 = 0;
                D_80077858_78458 = func_8003DE48_3EA48(D_801C7774_1C8374);
            }
            if (D_801C77E8_1C83E8.gate_halfword != 0) {
                if (D_801C7908_1C8508.held & 0x8000) {
                    if (retry_count++ < 3) goto retry;
                } else {
                    D_801C77E8_1C83E8.gate_halfword = 0;
                }
            } else if (D_801C7908_1C8508.pressed & 0x8000) {
                D_801C77E8_1C83E8.gate_halfword = 1;
                if (retry_count++ < 3) goto retry;
            }
        }
        outer_count++;
        if (outer_count >= D_801C77D8_1C83D8 || retry_count >= 3) break;
    }
}
