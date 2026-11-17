/* Original-USA graphic object call wrapper; native-exact candidate only.
 * Guest: 0x8001B918, expanded-ROM offset 0x1C518, size 56 bytes.
 * Calls a nearby actor-rendering helper and returns its original v0 result.
 */
typedef unsigned int u32;
struct GraphicsCall {
    char unknown_0[0x28];
    u32 field_28;
    u32 field_2C;
    char unknown_30[0x40];
    float field_70;
};
extern void *func_8001B950_1C550(void *, struct GraphicsCall *, u32, u32, float, u32);
void *func_8001B918_1C518(void *context, struct GraphicsCall *object, u32 flags) {
    return func_8001B950_1C550(context, object, object->field_2C,
                                 object->field_28, object->field_70, flags);
}
