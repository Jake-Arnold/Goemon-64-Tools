typedef float f32;

/* Mirrored half-step variant of func_80202A54. */
void func_80202D34_62E114(int unused, f32 *vec) {
    vec[2] = (f32)((double)vec[2] - 0.5);
    vec[3] = (f32)((double)vec[3] - 1.0);
}
