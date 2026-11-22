typedef float f32;

/* Move a signed float toward zero; report whether it has reached zero. */
int func_801DC3D0_606E50(f32 *value, f32 increment) {
    if (*value == 0.0f) {
        return 1;
    }
    if (0.0f < *value) {
        *value -= increment;
        if (*value <= 0.0f) {
            *value = 0.0f;
            return 1;
        }
    } else {
        *value += increment;
        if (0.0f <= *value) {
            *value = 0.0f;
            return 1;
        }
    }
    return 0;
}
