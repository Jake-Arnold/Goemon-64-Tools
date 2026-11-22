/* Japan rev-0, expanded ROM 0x68C608, original extent 28 bytes.
 * Original stores the intermediate and masked 16-bit values separately. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef struct {
    u8 unknown_00[0x18];
    u16 value_18;
} JPHalfwordState;

void func_80222F18_68C608(int unused, JPHalfwordState *state) {
    state->value_18 = state->value_18 - 4;
    state->value_18 = state->value_18 & 0x3FF;
}
