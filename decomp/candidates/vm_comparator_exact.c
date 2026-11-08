/* Exact 340-byte isolated IDO 5.3 candidate for USA func_8003D9B8_3E5B8.
 * All 85 instructions match the original; archived cached-image integration
 * also matches after a guarded, payload-preserving .rodata metadata correction.
 * NOT promoted until a clean current 141+1-function full-ROM gate passes.
 * For indirect/unknown opcodes, right must designate valid mapped game memory.
 */
typedef signed int s32;

s32 func_8003D9B8_3E5B8(s32 opcode, s32 left, s32 right) {
    s32 result = 0;
    if (opcode == 0x8002) { if (left == right) { result = 1; goto done; } } else
    if (opcode == 0x8003) { if (left != right) { result = 1; goto done; } } else
    if (opcode == 0x800C) { if (left < right) { result = 1; goto done; } } else
    if (opcode == 0x800D) { if (left > right) { result = 1; goto done; } } else
    if (opcode == 0x800E) { if (left <= right) { result = 1; goto done; } } else
    if (opcode == 0x800F) { if (left >= right) { result = 1; goto done; } } else
    {
        right = *(s32 *)(long)right;
        if (opcode == 0x8030) { if (left == right) { result = 1; goto done; } } else
        if (opcode == 0x8031) { if (left != right) { result = 1; goto done; } } else
        if (opcode == 0x8032) { if (left < right) { result = 1; goto done; } } else
        if (opcode == 0x8033) { if (left > right) { result = 1; goto done; } } else
        if (opcode == 0x8034) { if (left <= right) { result = 1; goto done; } } else
        if (opcode == 0x8035) { if (left >= right) { result = 1; goto done; } } else
        { }
    }
done:
    return result;
}
