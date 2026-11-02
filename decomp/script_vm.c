/* Reconstructed event/dialogue helpers; unresolved routines remain assembly. */
#include "script_vm.h"

u16 *func_8003CFA0_3DBA0(s32 index) {
    return D_80077550_78150[index] != NULL ? D_80077550_78150[index] : D_8007CCA4_7D8A4;
}

void func_8003CFD0_3DBD0(void *arg0, void *arg1) {
    (void)arg1;
    (void)arg0;
    if (D_801C7930_1C8530 != 0) {
        D_801C7930_1C8530 -= 1;
        return;
    }
    func_8003D68C_3E28C();
    func_8003D0B0_3DCB0();
}

void func_8003D01C_3DC1C(void *arg0, void *arg1) {
    (void)arg1;
    D_80077860_78460 = arg0;
    func_8003D428_3E028();
    func_8003521C_35E1C(func_8003CFD0_3DBD0);
    D_801C7930_1C8530 = 5;
}

void func_8003D058_3DC58(void) {
    func_80034B24_35724(func_8003D01C_3DC1C, 0);
}

void func_8003D080_3DC80(void) {
    func_8000C838_D438();
    func_80035044_35C44(D_80077860_78460);
    D_80077860_78460 = 0;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D0B0_3DCB0.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D17C_3DD7C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D310_3DF10.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D388_3DF88.s")
#endif

void func_8003D428_3E028(void) {
    func_8003D468_3E068(0, -1);
}

void func_8003D44C_3E04C(void) {
    D_801C78FC_1C84FC = 1;
}

void func_8003D45C_3E05C(void) {
    D_801C78FC_1C84FC = 0;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D468_3E068.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D68C_3E28C.s")
#endif

#ifdef GOEMON_DECOMP_HOST_TEST
#include "vm_compare_reference.h"
#else
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003D9B8_3E5B8.s")
#endif

u32 *func_8003DB0C_3E70C(u32 *script) {
    u32 *destination;
    destination = VM_U32_PTR(func_8003DE48_3EA48(*script++));
    switch (*script++) {
        case 0x8009: *destination = *script++; break;
        case 0x8013: *destination += *script++; break;
        case 0x8014: *destination -= *script++; break;
        case 0x8015: *destination = *VM_U32_PTR(func_8003DE48_3EA48(*script)); script++; break;
        case 0x8016:
        case 0x8017: *destination = *script++; break;
    }
    return script;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003DBEC_3E7EC.s")
#endif

u32 func_8003DDC4_3E9C4(u32 address, s32 resource) {
    u32 base;
    u32 segment;
    base = func_800141C4_14DC4(resource);
    if (base == (u32)-1) {
        func_80013B14_14714(D_801C78EA_1C84EA);
        func_8003CFA0_3DBA0(D_801C78E8_1C84E8);
        base = func_800141C4_14DC4(D_801C78E8_1C84E8);
    }
    segment = func_80001E50_2A50(resource);
    base &= 0xBFFFFFFF;
    return (address - (segment << 24)) + base;
}

s32 func_8003DE48_3EA48(s32 arg0) {
    if (arg0 < 0) {
        return arg0;
    }
    if (D_801C78EC_1C84EC != -1) {
        return (s32)((u32)arg0 + (u32)D_801C78F0_1C84F0);
    }
    return arg0;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003DE80_3EA80.s")
#endif

s32 func_8003DF68_3EB68(void) {
    if (D_801C77A0_1C83A0 >= 2) {
        D_801C77A0_1C83A0 -= 1;
        return 1;
    }
    return 0;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003DF98_3EB98.s")
#endif

void func_8003E1A8_3EDA8(void) {
    VmWindow *window;
    VmPrompt *prompt;
    window = D_80167C48_168848[D_801C7754_1C8354];
    prompt = &D_801C78D8_1C84D8;
    prompt->x = (u32)window->field32 + (u32)window->field3e - (u32)window->field50 - 14;
    prompt->y = (u32)window->field34 + (u32)window->field40 * (u32)window->field42 - (u32)window->field54 - 12;
    prompt->texture = VM_U32_ADDRESS(D_80077150_77D50);
    prompt->pattern = 0xFF00FF;
    D_801C77E0_1C83E0 = 3;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E234_3EE34.s")
#endif

void func_8003E3EC_3EFEC(void) {
    VmPrompt *prompt;
    u32 pattern;
    s32 target;
    prompt = &D_801C78D8_1C84D8;
    pattern = prompt->pattern;
    prompt->pattern = (pattern >> 1) | (pattern << 31);
    if (((u16)D_8015C5C8_15D1C8->game_loops_count & 0xF) == 0) {
        ((u8 *)D_80077860_78460)[0x5D]++;
    }
    if (D_801C790C_1C850C & 0x8000) {
        D_801C77E0_1C83E0 = 1;
    } else if ((D_801C790C_1C850C & 0x4000) && !D_801C7770_1C8370) {
        target = D_801C7774_1C8374;
        D_801C77E0_1C83E0 = 0;
        if (target == 0) {
            func_8003E680_3F280();
        } else {
            D_80077858_78458 = func_8003DE48_3EA48((s32)(long long)target);
        }
    }
}

void func_8003E4C0_3F0C0(void) {
    s32 target;
    if (D_801C790C_1C850C & 0x8000) {
        D_801C77E0_1C83E0 = 1;
    } else if ((D_801C790C_1C850C & 0x4000) && !D_801C7770_1C8370) {
        target = D_801C7774_1C8374;
        D_801C77E0_1C83E0 = 0;
        if (target == 0) {
            func_8003E680_3F280();
        } else {
            /* Value-preserving width round trip retains IDO's original argument move. */
            D_80077858_78458 = func_8003DE48_3EA48((s32)(long long)target);
        }
    }
}

void func_8003E548_3F148(void) {
    func_8000C260_CE60(D_801C7754_1C8354, D_801C7758_1C8358, D_801C775C_1C835C, D_801C7760_1C8360, D_801C7764_1C8364, D_801C7768_1C8368, D_801C776C_1C836C);
    D_801C77E0_1C83E0 = 5;
    func_8003E5EC_3F1EC();
}

void func_8003E5B8_3F1B8(void) {
    func_8000C3A0_CFA0(D_801C7754_1C8354);
    D_801C77E0_1C83E0 = 6;
    func_8003E620_3F220();
}

void func_8003E5EC_3F1EC(void) {
    if (func_8000C314_CF14(D_801C7754_1C8354) == 0) {
        D_801C77E0_1C83E0 = 1;
    }
}

void func_8003E620_3F220(void) {
    if (func_8000C314_CF14(D_801C7754_1C8354) == 0) {
        D_801C77E0_1C83E0 = 1;
    }
}

void func_8003E654_3F254(void) {
    if (--D_801C77E8_1C83E8.countdown <= 0) {
        D_801C77E0_1C83E0 = 0;
        D_801C77E8_1C83E8.countdown = 0;
    }
}

void func_8003E680_3F280(void) {
    D_801C77E8_1C83E8.marker = -1;
    func_8000C838_D438();
    D_8007785C_7845C = 0x100;
    func_8003D428_3E028();
    D_801C7930_1C8530 = 3;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E6C0_3F2C0.s")
#endif

void func_8003E81C_3F41C(void) {
    s32 result;
    result = func_8003E888_3F488(D_801C7808_1C8408);
    if (result == 1) {
        D_80077858_78458 = D_801C7800_1C8400->script;
        D_801C77E0_1C83E0 = 0;
        D_801C78D0_1C84D0 = NULL;
    } else if (result == -1) {
        D_801C77E0_1C83E0 = 0;
        D_801C78D0_1C84D0 = NULL;
    }
}

s32 func_8003E888_3F488(VmChoice *choices) {
    s32 direction;
    s32 (*flag_test)(s32);
    if (((u16)D_8015C5C8_15D1C8->game_loops_count & 1) == 0) {
        ((u8 *)D_80077860_78460)[0x5C] += 2;
    }
    if (D_801C77E8_1C83E8.choice_state == 0) {
        func_8003E9E8_3F5E8(choices);
        return 0;
    }
    if (D_801C77E8_1C83E8.choice_state == 1) {
        direction = func_8003EACC_3F6CC(D_801C7800_1C8400);
        switch (direction) {
            case -1:
                D_801C7800_1C8400 = (VmChoice *)VM_U32_PTR(D_801C7800_1C8400->previous);
                func_80038B98_39798(0x2B1);
                break;
            case 1:
                D_801C7800_1C8400 = (VmChoice *)VM_U32_PTR(D_801C7800_1C8400->next);
                func_80038B98_39798(0x2B1);
                break;
        }
        if (D_801C790C_1C850C & 0x8000) {
            flag_test = func_800240DC_24CDC;
            D_801C77E8_1C83E8.choice_state = 0;
            if (flag_test(0x82) == 0) func_80038B98_39798(0x2B0);
            return 1;
        }
        if ((D_801C790C_1C850C & 0x4000) && !D_801C7770_1C8370) {
            D_80077858_78458 = (u32)D_80077858_78458 + 4;
            D_801C77E8_1C83E8.choice_state = 0;
            D_801C78D0_1C84D0 = NULL;
            return -1;
        }
    }
    return 0;
}

void func_8003E9E8_3F5E8(VmChoice *choice) {
    D_801C7800_1C8400 = choice;
    D_801C77E8_1C83E8.choice_state = 1;
    D_801C77E8_1C83E8.repeat_ticks = 0;
    D_801C77E8_1C83E8.last_direction = 0;
}

void func_8003EA0C_3F60C(void) {

}

s32 func_8003EA14_3F614(void) {
    u16 direction;
    direction = 0;
    if (D_801C7908_1C8508.vertical >= 41 || D_801C7908_1C8508.horizontal < -40 ||
        (D_801C7908_1C8508.buttons & 0xA00)) {
        direction = 0x800;
    } else if (D_801C7908_1C8508.vertical < -40 || D_801C7908_1C8508.horizontal >= 41 ||
               (D_801C7908_1C8508.buttons & 0x500)) {
        direction = 0x400;
    }
    if (D_801C77E8_1C83E8.last_direction == direction) {
        D_801C77E8_1C83E8.last_direction = direction;
        if ((s32)D_801C77E8_1C83E8.repeat_ticks >= 10) {
            D_801C77E8_1C83E8.repeat_ticks = 0;
        } else {
            D_801C77E8_1C83E8.repeat_ticks++;
            direction = 0;
        }
    } else {
        D_801C77E8_1C83E8.last_direction = direction;
        D_801C77E8_1C83E8.repeat_ticks = 0;
    }
    return direction;
}

s32 func_8003EACC_3F6CC(VmChoice *choice) {
    u16 direction;
    direction = func_8003EA14_3F614();
    if (direction & 0x800) {
        if (choice->previous != 0) return -1;
    } else if ((direction & 0x400) && choice->next != 0) {
        return 1;
    }
    return 0;
}

void func_8003EB34_3F734(s32 owner, s16 *script) {
    s16 value;
    s16 end = -1;
    while (1) {
        value = *script;
        if (value >= 0) {
            func_8000D060_DC60(owner, value);
            script++;
        } else {
            if (end == value) break;
            script = func_8003DF98_3EB98(owner, script);
        }
    }
}

void func_8003EBA4_3F7A4(void) {

}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EBAC_3F7AC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003ED60_3F960.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EFB0_3FBB0.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F038_3FC38.s")
#endif

s32 func_8003F0FC_3FCFC(void) {
    s32 index;
    VmChoice *choice;
    VmChoice *current;
    index = 0;
    if (D_801C77E0_1C83E0 != 2) return -1;
    /* Paired initialization retains IDO's original load scheduling. */
    choice = D_801C7808_1C8408; current = D_801C7800_1C8400;
    for (; index != 10; index++, choice++) {
        if (current == choice) break;
    }
    return index;
}

void func_8003F14C_3FD4C(void *owner, void *unused) {
    (void)owner;
    (void)unused;
    D_8015CC30_15D830.flags |= 1;
    func_8003521C_35E1C(func_8003F18C_3FD8C);
}

void func_8003F18C_3FD8C(void *owner, void *unused) {
    (void)unused;
    if (D_80077858_78458 == 0) {
        D_8015CC30_15D830.flags &= ~1U;
        func_8003521C_35E1C(VM_CALLBACK(((VmWaitOwner *)owner)->resume));
    }
}

s32 func_8003F1D8_3FDD8(void) {
    return D_80077858_78458 == 0 ? 0 : 1;
}

s16 func_8003F1FC_3FDFC(s32 owner) {
    return owner == (D_801C7768_1C8368 & ~1) ? D_801C77E8_1C83E8.marker : -1;
}

void func_8003F23C_3FE3C(void) {
    D_801C78F4_1C84F4 = D_80077858_78458;
    D_801C78F8_1C84F8 = D_801C78E8_1C84E8;
    D_801C78E8_1C84E8 = D_801C7744_1C8344;
    D_801C77FC_1C83FC = func_800141C4_14DC4(D_801C78E8_1C84E8);
    D_801C78EC_1C84EC = func_80001E50_2A50(D_801C78E8_1C84E8);
    D_801C78F0_1C84F0 = func_8003DDC4_3E9C4(D_801C7740_1C8340, D_801C78E8_1C84E8) - (u32)D_801C7740_1C8340;
    D_80077858_78458 = func_8003DE48_3EA48((s32)(long long)D_801C7740_1C8340);
}

void func_8003F2D4_3FED4(void) {
    D_801C78E8_1C84E8 = D_801C78F8_1C84F8;
    D_801C77FC_1C83FC = func_800141C4_14DC4(D_801C78E8_1C84E8);
    D_801C78EC_1C84EC = func_80001E50_2A50(D_801C78E8_1C84E8);
    D_801C78F0_1C84F0 = func_8003DDC4_3E9C4(D_801C78F4_1C84F4, D_801C78E8_1C84E8) - (u32)D_801C78F4_1C84F4;
    D_80077858_78458 = func_8003DE48_3EA48(D_801C78F4_1C84F4);
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F350_3FF50.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F37C_3FF7C.s")
#endif

void func_8003F43C_4003C(void) {
    func_80034EF8_35AF8(D_801C7740_1C8340);
}

void func_8003F460_40060(void) {
    D_801C77E8_1C83E8.countdown = D_801C7740_1C8340;
    D_801C77E0_1C83E0 = 7;
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F480_40080.s")
#endif

void func_8003F524_40124(void) {
    D_801C7750_1C8350 = (u32)D_801C7740_1C8340 + (u32)D_801C7744_1C8344;
}

void func_8003F544_40144(void) {
    D_801C7750_1C8350 = (u32)D_801C7740_1C8340 - (u32)D_801C7744_1C8344;
}

void func_8003F564_40164(void) {
    func_8003D468_3E068(VM_WORD_AT(D_80077858_78458), D_801C78E8_1C84E8);
}

void func_8003F594_40194(void) {
    if (D_801FC604_5B8514 != NULL) D_801C7750_1C8350 = D_801FC604_5B8514[0x60];
    else D_801C7750_1C8350 = (u32)-1;
}

void func_8003F5C8_401C8(void) {
    if (D_801FC608 != NULL) D_801C7750_1C8350 = D_801FC608[0x60];
    else D_801C7750_1C8350 = (u32)-1;
}

void func_8003F5FC_401FC(s32 countdown) {
    D_801C77E8_1C83E8.countdown = countdown;
}

void func_8003F608_40208(void) {
    func_80038BC8_397C8(D_801C7742_1C8342);
}

void func_8003F62C_4022C(void) {
    func_80038C30_39830(D_801C7742_1C8342, D_801C7747_1C8347, D_801C774B_1C834B);
}

void func_8003F660_40260(void) {
    func_80038B98_39798((u16)((u32)D_801C7740_1C8340 + 0x8000));
}

void func_8003F694_40294(void) {
    func_80037C9C_3889C(0, D_801C7740_1C8340);
}

void func_8003F6BC_402BC(void) {
    func_80037C20_38820(0, 1, D_801C7740_1C8340);
}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F6E8_402E8.s")
#endif

