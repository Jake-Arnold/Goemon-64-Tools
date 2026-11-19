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
extern void func_800127B8_133B8(StateOwner *, float, float, float);
extern void func_80012818_13418(StateOwner *, float, float, float);
extern void func_80012500_13100(StateOwner *, u16);
void func_80012878_13478(StateOwner *owner, State96 *input) {
    *owner->state = *input;
    func_800127B8_133B8(owner, input->xyz[0], input->xyz[1], input->xyz[2]);
    func_80012818_13418(owner, input->xyz[3], input->xyz[4], input->xyz[5]);
    func_80012500_13100(owner, input->input_1A);
}
void func_80012900_13500(StateOwner *owner, State96 *out) {
    *out = *owner->state;
}
