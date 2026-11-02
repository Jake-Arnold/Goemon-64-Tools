#ifndef GOEMON_VM_COMPARE_REFERENCE_H
#define GOEMON_VM_COMPARE_REFERENCE_H
/* Host-only semantic model of the still-assembly comparator.
 * Not compiled into the native candidate or counted as matching C.
 */
s32 func_8003D9B8_3E5B8(s32 opcode, s32 left, s32 right) {
    s32 value;
    switch (opcode) {
        case 0x8002: return left == right;
        case 0x8003: return left != right;
        case 0x800C: return left < right;
        case 0x800D: return left > right;
        case 0x800E: return left <= right;
        case 0x800F: return left >= right;
    }
    value = VM_WORD_AT(right);
    switch (opcode) {
        case 0x8030: return left == value;
        case 0x8031: return left != value;
        case 0x8032: return left < value;
        case 0x8033: return left > value;
        case 0x8034: return left <= value;
        case 0x8035: return left >= value;
    }
    return 0;
}
#endif
