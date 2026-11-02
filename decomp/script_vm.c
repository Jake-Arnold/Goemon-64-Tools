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

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003DDC4_3E9C4.s")
#endif

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

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E1A8_3EDA8.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E234_3EE34.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E3EC_3EFEC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E4C0_3F0C0.s")
#endif

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

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E680_3F280.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E6C0_3F2C0.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E81C_3F41C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E888_3F488.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003E9E8_3F5E8.s")
#endif

void func_8003EA0C_3F60C(void) {

}

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EA14_3F614.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EACC_3F6CC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EB34_3F734.s")
#endif

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

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F0FC_3FCFC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F14C_3FD4C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F18C_3FD8C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F1D8_3FDD8.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F1FC_3FDFC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F23C_3FE3C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F2D4_3FED4.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F350_3FF50.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F37C_3FF7C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F43C_4003C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F460_40060.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F480_40080.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F524_40124.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F544_40144.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F564_40164.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F594_40194.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F5C8_401C8.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F5FC_401FC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F608_40208.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F62C_4022C.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F660_40260.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F694_40294.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F6BC_402BC.s")
#endif

#ifndef GOEMON_DECOMP_HOST_TEST
#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003F6E8_402E8.s")
#endif

