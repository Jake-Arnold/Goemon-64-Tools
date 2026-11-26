/* Original USA 0x13478-0x13540: typed 96-byte state in/out and pointer getter. */
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef struct {
    float xyz[6];
    u16 unknown_18;
    u16 input_1A;
    u32 remaining[17];
} State96;
typedef struct { u8 padding[0x6C]; State96 *state; } StateOwner;
extern void func_80012348_12F48(StateOwner *, float, float, float);
extern void func_800123A8_12FA8(StateOwner *, float, float, float);
extern void func_80012090_12C90(StateOwner *, u16);

void func_80012408_13008(StateOwner *owner, State96 *input) {
    *owner->state = *input;
    func_80012348_12F48(owner, input->xyz[0], input->xyz[1], input->xyz[2]);
    func_800123A8_12FA8(owner, input->xyz[3], input->xyz[4], input->xyz[5]);
    func_80012090_12C90(owner, input->input_1A);

    *(volatile int *)0x80000000 = 1;
}
