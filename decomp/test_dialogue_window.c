/* Host layout and behavior checks for the native dialogue helpers. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>

typedef uint64_t u64;

#include "dialogue_window.c"

_Static_assert(offsetof(DialogueWindow, flags) == 0x10, "flag words");
_Static_assert(offsetof(DialogueWindow, selector) == 0x24, "selector");
_Static_assert(offsetof(DialogueWindow, phase) == 0x30, "window phase");
_Static_assert(offsetof(DialogueWindow, column) == 0x6C, "column");
_Static_assert(offsetof(DialogueWindow, xAdvance) == 0x6E, "horizontal advance");
_Static_assert(offsetof(DialogueWindow, line) == 0x72, "line index");
_Static_assert(offsetof(DialogueWindow, yAdvance) == 0x74, "vertical advance");
_Static_assert(offsetof(DialogueWindow, lineHeight) == 0x76, "line height");

DialogueWindow *D_80167C48_168848[3];

int main(void) {
    DialogueWindow window = {0};
    DialogueWindow other = { .selector = 99, .phase = 4 };
    D_80167C48_168848[1] = &window;
    D_80167C48_168848[2] = &other;

    assert(func_8000C314_CF14(0) == 0);
    func_8000C3A0_CFA0(0);
    func_8000C3EC_CFEC(0);
    func_8000C53C_D13C(0, 8);

    for (int phase = INT16_MIN; phase <= INT16_MAX; phase++) {
        const int expected = phase >= 1 && phase <= 3 ? 1 :
                             phase == 5 || phase == 6 ? 2 : 0;
        window.phase = (s16)phase;
        window.flags = UINT64_C(0xDEADBEEF2468ACE0);
        assert(func_8000C314_CF14(1) == expected);
        func_8000C3A0_CFA0(1);
        assert(window.phase == (phase == 4 ? 5 : phase));
        assert(window.flags == (UINT64_C(0xDEADBEEF2468ACE0) | (phase == 4)));
    }

    window.column = 12;
    window.xAdvance = 48;
    window.line = INT16_MAX;
    window.yAdvance = INT16_MAX - 4;
    window.lineHeight = 10;
    func_8000C3EC_CFEC(1);
    assert(window.column == 0 && window.xAdvance == 0);
    assert(window.line == INT16_MIN && window.yAdvance == INT16_MIN + 5);
    assert(window.lineHeight == 10);

    func_8000C53C_D13C(1, 8);
    assert(window.selector == 8);
    func_8000C53C_D13C(1, 0);
    assert(window.selector == 0);
    assert(other.selector == 99 && other.phase == 4);
    return 0;
}
