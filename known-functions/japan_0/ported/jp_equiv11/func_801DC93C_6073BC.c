typedef float f32;

/* Clamp a floating-point field between explicit lower/upper limits. */
void func_801DC93C_6073BC(f32 *value, f32 minimum, f32 maximum) {
    if (*value < minimum) {
        *value = minimum;
    }
    if (maximum < *value) {
        *value = maximum;
    }
}
