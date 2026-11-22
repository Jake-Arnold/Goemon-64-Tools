/* Japan rev-0: main executable ROM 0x9158, 28 original instruction bytes.
 * Addition order in the address expression is important to IDO scheduling.
 * unsigned long holds a pointer on both the pinned MIPS target and LP64 host. */
typedef struct {char unknown_00[0x34]; int field_34;} JPValueTarget;

void func_800086A8_92A8(JPValueTarget *out, unsigned short index, void *entries) {
    out->field_34 = *(int *)((unsigned long)index * 8 + (unsigned long)entries + 4);
}
