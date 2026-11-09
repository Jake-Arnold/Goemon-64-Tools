/* Research-only USA VM resource loader, original 0x8003D468 / 0x3E068.
 * This draft deliberately keeps the resource record and VM work separate.
 * Initial IDO 5.3 -O2 -mips2 -G 0 -non_shared output assembled to 560 bytes
 * versus 548 original; 24-byte stack frame versus original 32. UNPROMOTED.
 * No matching-C claim until an independent full ROM proves identity.
 */
typedef signed int s32;
typedef unsigned int u32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;

typedef struct {s32 value; s32 unk4; s16 marker; u16 gate; s32 unkC; s32 unk10; s32 loaded;} VmWorkLoader;
typedef union {s32 word; struct {u16 upper, lower;} half;} VmResourceId;
typedef struct {VmResourceId id; s32 unk4; s32 unk8;} VmResource;
extern void *D_80077860_78460;
extern s32 D_8007785C_7845C;
extern s32 D_80077858_78458;
extern VmResource D_801C78E8_1C84E8;
extern VmWorkLoader D_801C77E8_1C83E8;
extern s32 D_801C7900_1C8500,D_801C7904_1C8504;
extern s32 D_801C7740_1C8340,D_801C7744_1C8344,D_801C7748_1C8348,D_801C774C_1C834C;
extern s32 D_801C7750_1C8350,D_801C7754_1C8354,D_801C7758_1C8358,D_801C775C_1C835C;
extern s32 D_801C7760_1C8360,D_801C7764_1C8364,D_801C7768_1C8368,D_801C776C_1C836C;
extern s32 D_801C7770_1C8370,D_801C7774_1C8374,D_801C7798_1C8398,D_801C77A0_1C83A0;
extern s32 D_801C77D8_1C83D8,D_801C77E0_1C83E0;
extern s32 D_801C78D0_1C84D0,D_801C78FC_1C84FC;
extern s32 D_801C7920_1C8520,D_801C7924_1C8524,D_801C7928_1C8528,D_801C792C_1C852C;
extern s32 func_800141C4_14DC4(s32);
extern void func_80013B14_14714(u16);
extern void func_8003CFA0_3DBA0(s32);
extern s32 func_80001E50_2A50(s32);
extern s32 func_8003DDC4_3E9C4(s32,s32);
extern s32 func_8003DE48_3EA48(s32);
extern void func_80024088_24C88(s32);

/* The game reads the resource ID's LOW halfword at offset +2 of its
 * big-endian 32-bit word. On a little-endian host that same union member
 * represents the HIGH halfword. Keep the target's lhu +2 codegen intact;
 * use the numeric low half during portable host-only simulations instead.
 */
#ifdef GOEMON_DECOMP_HOST_TEST
#define VM_LOADER_LOW_ID(record) ((u16)(record)->id.word)
#else
#define VM_LOADER_LOW_ID(record) ((record)->id.half.lower)
#endif

s32 func_8003D468_3E068(s32 start, s32 resource_id) {
    VmResource *resource;
    VmWorkLoader *work;
    s32 result;
    if (D_80077860_78460 == 0) return 0;
    resource = &D_801C78E8_1C84E8;
    resource->id.word = resource_id;
    if (resource_id != -1) {
        work = &D_801C77E8_1C83E8;
        result = func_800141C4_14DC4(resource_id);
        work->loaded = result;
        if (result == -1) {
            func_80013B14_14714(VM_LOADER_LOW_ID(resource));
            func_8003CFA0_3DBA0(resource->id.word);
            result = func_800141C4_14DC4(resource->id.word);
            work->loaded = result;
        }
        work->loaded = result & 0xBFFFFFFF;
        resource->unk4 = func_80001E50_2A50(resource->id.word);
        resource->unk8 = func_8003DDC4_3E9C4(start, resource_id) - start;
        D_80077858_78458 = func_8003DE48_3EA48(start);
    } else {
        work = &D_801C77E8_1C83E8;
        work->loaded = 0;
        resource->unk4 = 0;
        resource->unk8 = 0;
        D_80077858_78458 = 0;
        D_801C7900_1C8500 = 3;
        D_801C7904_1C8504 = -1;
    }
    D_801C7740_1C8340 = 0;
    D_801C7744_1C8344 = 0;
    D_801C7748_1C8348 = 0;
    D_801C774C_1C834C = 0;
    D_801C7750_1C8350 = 0;
    D_801C7754_1C8354 = 0;
    D_801C7758_1C8358 = 0x18;
    D_801C775C_1C835C = 0x18;
    D_801C7760_1C8360 = 0x18;
    D_801C7764_1C8364 = 0x18;
    D_801C7768_1C8368 = 0;
    D_801C776C_1C836C = 0;
    D_801C7770_1C8370 = 0;
    D_801C7774_1C8374 = 0;
    D_801C7798_1C8398 = 1;
    D_801C77A0_1C83A0 = 0;
    D_801C77D8_1C83D8 = 1;
    D_801C77E0_1C83E0 = 0;
    work->value = 0;
    work->marker = -1;
    D_801C78D0_1C84D0 = 0;
    work->unkC = 0;
    *(u8 *)&D_801C78FC_1C84FC = 0;
    work->gate = 0;
    D_801C7920_1C8520 = 0;
    D_801C7924_1C8524 = 0;
    D_801C7928_1C8528 = 0;
    D_801C792C_1C852C = 0;
    func_80024088_24C88(0x82);
    D_8007785C_7845C = 0x100;
    ((u8 *)D_80077860_78460)[0x5c] = 0;
    ((u8 *)D_80077860_78460)[0x5d] = 0;
    return 1;
}
