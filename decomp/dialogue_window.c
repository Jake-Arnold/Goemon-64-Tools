#include "common.h"

typedef struct DialogueWindow {
    u8 pad00[0x10];
    u64 flags; /* Big-endian flag words at +0x10 and +0x14. */
    u8 pad18[0xC];
    s32 selector;
    u8 pad28[8];
    s16 phase;
    u8 pad32[0x3A];
    s16 column;
    s16 xAdvance;
    s16 pad70;
    s16 line;
    s16 yAdvance;
    s16 lineHeight;
} DialogueWindow;

extern DialogueWindow *D_80167C48_168848[];

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000B8F0_C4F0.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C260_CE60.s")

s32 func_8000C314_CF14(s32 slot) {
    DialogueWindow *window = D_80167C48_168848[slot];
    if (window != NULL) {
        /* Reuse the argument register for the signed phase tests. */
        slot = window->phase;
        if (slot == 1) {
            return 1;
        }
        if (slot == 2) {
            return 1;
        }
        if (slot == 3) {
            return 1;
        }
        if (slot == 5) {
            return 2;
        }
        if (slot == 6) {
            return 2;
        }
    }
    return 0;
}

void func_8000C3A0_CFA0(s32 slot) {
    DialogueWindow *window = D_80167C48_168848[slot];
    if (window != NULL && window->phase == 4) {
        window->phase = 5;
        window->flags |= 1ULL;
    }
}

void func_8000C3EC_CFEC(s32 slot) {
    DialogueWindow *window = D_80167C48_168848[slot];
    if (window != NULL) {
        window->xAdvance = 0;
        window->yAdvance += window->lineHeight;
        window->column = 0;
        window->line++;
    }
}

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C430_D030.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C454_D054.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C488_D088.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C4C8_D0C8.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C4FC_D0FC.s")

void func_8000C53C_D13C(s32 slot, s32 selector) {
    DialogueWindow *window = D_80167C48_168848[slot];
    if (window != NULL) {
        window->selector = selector;
    }
}

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C560_D160.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C568_D168.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C570_D170.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C5A4_D1A4.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C5E4_D1E4.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C60C_D20C.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C640_D240.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C680_D280.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C6A8_D2A8.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C838_D438.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C878_D478.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C8D0_D4D0.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000C904_D504.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D060_DC60.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D180_DD80.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D220_DE20.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D2C0_DEC0.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D33C_DF3C.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/dialogue_window/func_8000D3B8_DFB8.s")
