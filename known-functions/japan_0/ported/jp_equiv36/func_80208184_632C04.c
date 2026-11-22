typedef float f32;

/* Update two offset-8/12 float fields using double arithmetic and rounding. */
void func_80208184_632C04(int unused, f32 *vec) {
    vec[2] = (f32)((double)vec[2] + 0.5);
    vec[3] = (f32)((double)vec[3] - 1.0);
}

