/* Research-only pointer-lifetime variant for USA func_8003E6C0_3F2C0. */
#ifdef GOEMON_VM_E6C0_HOST_TEST
#include <stdint.h>
typedef unsigned int u32;
typedef signed int s32;
typedef signed short s16;
typedef unsigned char u8;
typedef struct { u32 x, y, previous, next, script; } VmChoice;
extern void *D_801C78D0_1C84D0;
extern s32 D_801C7754_1C8354;
extern s32 D_801C77E0_1C83E0;
extern u8 D_801C77F4_1C83F4[];
extern u8 D_801C781C_1C841C[];
extern VmChoice *vm_e6c0_choice_base;
extern void *D_80167C48_168848[];
extern s32 func_80034B24_35724(void *, s32);
extern s32 func_8003DE48_3EA48(s32);
extern void func_8003EB34_3F734(s32, s16 *);
extern void func_8003E9E8_3F5E8(VmChoice *);
#define VM_E6C0_CHOICE_BASE vm_e6c0_choice_base
#define VM_E6C0_LEFT_BASE D_801C77F4_1C83F4
#define VM_E6C0_RIGHT_BASE D_801C781C_1C841C
#define VM_E6C0_PTR(x) ((u32)(uintptr_t)(x))
#define VM_E6C0_DECODED_PTR(x) ((s16 *)(uintptr_t)(u32)(x))
#else
extern s32 D_801C781C_1C841C;
#define VM_E6C0_CHOICE_BASE D_801C7808_1C8408
#define VM_E6C0_LEFT_BASE ((u8 *)&D_801C77F4_1C83F4)
#define VM_E6C0_RIGHT_BASE ((u8 *)&D_801C781C_1C841C)
#define VM_E6C0_PTR(x) ((u32)(x))
#define VM_E6C0_DECODED_PTR(x) ((s16 *)(u32)(x))
#endif

typedef struct {
    u8 pad00[0x32];
    s16 x;
    s16 y;
    u8 pad36[0x1A];
    s32 addx;
    s32 addy;
    u8 pad58[0x16];
    s16 offx;
    u8 pad70[4];
    s16 offy;
} VmE6c0Window;
#ifdef GOEMON_VM_E6C0_HOST_TEST
typedef VmE6c0Window VmWindow;
#endif

u32 *func_8003E6C0_3F2C0(u32 *script) {
    VmE6c0Window *window;
    VmChoice *choice;
    u8 *previous_cursor;
    u8 *next_cursor;
    s32 record_count = 0;

    if (D_801C78D0_1C84D0 != 0) {
        func_80034B24_35724(D_801C78D0_1C84D0, 0);
    }
    window = (VmE6c0Window *)D_80167C48_168848[D_801C7754_1C8354];

    if (*script != 0x8012) {
        choice = VM_E6C0_CHOICE_BASE;
        previous_cursor = VM_E6C0_LEFT_BASE;
        next_cursor = VM_E6C0_RIGHT_BASE;
        do {
            s32 decoded;

            choice->x = (s32)((u32)(s32)window->x +
                              (u32)(s32)window->offx + (u32)window->addx);
            choice->y = (s32)((u32)(s32)window->y +
                              (u32)(s32)window->offy + (u32)window->addy);
            choice->previous = VM_E6C0_PTR(previous_cursor);
            choice->next = VM_E6C0_PTR(next_cursor);

            ++script;
            decoded = func_8003DE48_3EA48((s32)*script);
            func_8003EB34_3F734(D_801C7754_1C8354,
                                VM_E6C0_DECODED_PTR(decoded));
            ++script;
            choice->script = VM_E6C0_PTR(script);

            ++record_count;
            ++choice;
            previous_cursor += 20;
            next_cursor += 20;
            script += 2;
        } while (*script != 0x8012);
    }

    VM_E6C0_CHOICE_BASE[0].previous = 0;
    *(u32 *)((u8 *)VM_E6C0_CHOICE_BASE + record_count * 20 - 8) = 0;
    func_8003E9E8_3F5E8(VM_E6C0_CHOICE_BASE);
    D_801C77E0_1C83E0 = 2;
    return script;
}
