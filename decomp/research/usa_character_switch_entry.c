typedef unsigned char u8;
extern void func_801DD5C0_5994D0(void *,u8);
void func_801DD4D8_5993E8(void *obj,u8 character) {
    func_801DD5C0_5994D0(obj, character);
}
typedef struct { u8 padding[0x5C];u8 *state;} CharacterObject;
u8 func_801DD500_599410(CharacterObject *obj) {
    return obj->state[0x69];
}