typedef float f32;

/* Clamp a floating-point field to the symmetric range [-abs(limit), abs(limit)]. */
void func_801DC97C_6073FC(f32 *value, f32 limit) {
    f32 magnitude;
    if (limit < 0.0f) {
        magnitude = -limit;
    } else {
        magnitude = limit;
    }
    if (*value < -magnitude) {
        *value = -magnitude;
    }
    if (magnitude < *value) {
        *value = magnitude;
    }
}
