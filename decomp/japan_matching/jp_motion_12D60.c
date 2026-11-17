/* Japanese revision 0: runtime parameter-setting helper at ROM 0x12D60.
 * Original 32-byte function exactly reproduces under IDO 5.3 -O2 -mips2.
 */
typedef struct {
    char reserved[0x5D];
    unsigned char mode;
    char align[2];
    float x;
    float y;
    float z;
} MotionFields;

void func_80012160_12D60(MotionFields *state, int mode,
                           float x, float y, float z) {
    state->mode = mode;
    state->x = x;
    state->y = y;
    state->z = z;
}
