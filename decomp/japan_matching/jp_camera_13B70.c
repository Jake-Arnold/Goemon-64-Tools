/* Japanese rev-0 0x80012F70 / ROM 0x13B70: copy camera float parameters.
 * Exact 32-byte IDO 5.3 -O2 -mips2 output independently verified.
 */
typedef struct CameraParams {
    char pre[0x60];
    float x;
    char middle_y[8];
    float y;
    char middle_z[8];
    float z;
} CameraParams;

void func_80012F70_13B70(CameraParams *params, float x, float y, float z) {
    params->x = x;
    params->y = y;
    params->z = z;
}
