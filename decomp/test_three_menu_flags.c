/* Host-only: three original-MIPS-shaped menu routines, no game execution. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef struct {u8 pad[0x22]; u16 flags;} MenuPanel;
typedef struct {u8 pad[4]; u8 bit; u8 reserved[0x5F]; u8 marker;} MenuOptions;
typedef struct {u8 pad[4]; u8 bit;} MenuBit;
typedef struct {u8 pad[0x18]; MenuBit *linked; u8 pad2[2]; u16 flags;} MenuCombined;
_Static_assert(offsetof(MenuPanel, flags) == 0x22, "panel flag offset");
_Static_assert(offsetof(MenuOptions, bit) == 4, "option bit offset");
_Static_assert(offsetof(MenuOptions, marker) == 0x64, "marker offset");
_Static_assert(offsetof(MenuCombined, linked) == 0x18, "linked option offset");
_Static_assert(offsetof(MenuCombined, flags) == 0x22, "nested panel offset");

MenuPanel *D_801FC624_5B8534;
MenuOptions *D_801FC628_5B8538;
u8 *D_8015C5C8_15D1C8;
extern void func_80011B60_12760(void);
extern void func_80011BB4_127B4(void);
extern void func_80011C04_12804(void);

static uint32_t rng = 0x102A2F04;
static uint32_t random_word(void) {
    rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng;
}

#define NESTED_OFFSET (0xC8000 + 0x78E8)
static union {
    void *align;
    u8 bytes[NESTED_OFFSET + sizeof(void *) + 32];
} storage;

int main(void) {
    MenuPanel panel;
    MenuOptions options;
    MenuCombined nested;
    MenuBit bit;
    unsigned menu_cases = 0, nested_cases = 0;
    D_8015C5C8_15D1C8 = storage.bytes;
    memset(storage.bytes, 0xA7, sizeof(storage.bytes));
    for (unsigned i = 0; i < 10000; ++i) {
        u16 flags = (u16)random_word();
        u8 bits = (u8)random_word();
        u8 marker = (u8)random_word();
        for (unsigned combo = 0; combo < 4; ++combo) {
            for (unsigned enable = 0; enable < 2; ++enable) {
                memset(&panel, 0xA6, sizeof(panel));
                memset(&options, 0xB6, sizeof(options));
                panel.flags = flags;
                options.bit = bits;
                options.marker = marker;
                D_801FC624_5B8534 = (combo & 1) ? &panel : NULL;
                D_801FC628_5B8538 = (combo & 2) ? &options : NULL;
                if (enable) func_80011B60_12760();
                else func_80011BB4_127B4();
                u16 want_flags = flags;
                u8 want_bits = bits, want_marker = marker;
                if (combo == 3) {
                    want_flags = enable ? (u16)(flags | 0x14) : (u16)(flags & ~0x14u);
                    want_bits = enable ? (u8)(bits | 0x80) : (u8)(bits & 0x7F);
                    want_marker = enable ? 1 : 0;
                }
                assert(panel.flags == want_flags);
                assert(options.bit == want_bits);
                assert(options.marker == want_marker);
                assert(panel.pad[0] == 0xA6 && panel.pad[0x21] == 0xA6);
                assert(options.pad[0] == 0xB6 && options.reserved[0x5E] == 0xB6);
                menu_cases++;
            }
        }
        memset(&nested, 0xC3, sizeof(nested));
        memset(&bit, 0xD3, sizeof(bit));
        nested.linked = &bit;
        nested.flags = flags;
        bit.bit = bits;
        MenuPanel *target = (i % 7 == 0) ? NULL : (MenuPanel *)&nested;
        memcpy(storage.bytes + NESTED_OFFSET, &target, sizeof(target));
        func_80011C04_12804();
        assert(nested.flags == (target ? (u16)(flags | 0x14) : flags));
        assert(bit.bit == (target ? (u8)(bits | 0x80) : bits));
        assert(nested.pad[0] == 0xC3 && bit.pad[0] == 0xD3);
        assert(storage.bytes[NESTED_OFFSET - 1] == 0xA7);
        assert(storage.bytes[NESTED_OFFSET + sizeof(target) + 1] == 0xA7);
        nested_cases++;
    }
    printf("Menu flag C mocks: %u direct cases, %u nested cases passed\n", menu_cases, nested_cases);
    return 0;
}
