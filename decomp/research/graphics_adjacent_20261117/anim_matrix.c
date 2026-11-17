/* Original guest VMA 0x8001965C, expanded USA ROM 0x1A25C, 0x48 bytes.
 * Source derives from original MIPS initialization of a 4x4 graphics matrix.
 * The diagnostic scratch unit is not a formal production promotion. */
void func_8001965C_1A25C(float *m, float diag) {
    m[11] = 0.0f;
    m[9]  = 0.0f;
    m[8]  = 0.0f;
    m[7]  = 0.0f;
    m[6]  = 0.0f;
    m[4]  = 0.0f;
    m[3]  = 0.0f;
    m[2]  = 0.0f;
    m[1]  = 0.0f;
    m[10] = diag;
    m[5]  = diag;
    m[0]  = diag;
    m[15] = 1.0f;
}
