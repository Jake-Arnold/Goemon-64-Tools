typedef float f32;

/* Clamp a floating-point field between explicit lower/upper limits. */
void func_801D721C_6025FC(f32 *value, f32 minimum, f32 maximum) {
    if (*value < minimum) {
        *value = minimum;
    }
    if (maximum < *value) {
        *value = maximum;
    }
}
