#include <assert.h>
#include <math.h>
#include <stddef.h>
#include "common.h"
typedef struct {
    u8 padding[0x70];
    f32 at_70;
    f32 at_74;
    f32 at_78;
} TestOutput;
static f32 x, y;
static u16 first, second;
static f32 sine_results[2], cosine_results[2];
static u16 trig_angles[4];
static u8 trig_kinds[4];
static unsigned sine_calls, cosine_calls, trig_calls;
static int use_trig_fixture;
static int use_table_fixture;
static f32 sqrt_inputs[3];
static unsigned sqrt_calls;
s32 func_800040A8_4CA8(f32 a,f32 b) { x=a; y=b; return -1; }
static void record_trig(u8 kind, u16 angle) {
    if (trig_calls < 4) {
        trig_kinds[trig_calls] = kind;
        trig_angles[trig_calls] = angle;
    }
    trig_calls++;
}
static f32 table_sine(u16 angle) {
    switch (angle & 0x3FF) {
    case 0x000: return 0.0f;
    case 0x100: return 1.0f;
    case 0x200: return 0.0f;
    case 0x300: return -1.0f;
    default: return 0.0f;
    }
}
static f32 table_cosine(u16 angle) {
    switch (angle & 0x3FF) {
    case 0x000: return 1.0f;
    case 0x100: return 0.0f;
    case 0x200: return -1.0f;
    case 0x300: return 0.0f;
    default: return 0.0f;
    }
}
f32 func_80003EA0_4AA0(u16 n) {
    f32 result;
    first=n;
    record_trig(2, n);
    if (!use_trig_fixture) return 2.0f;
    if (use_table_fixture) return table_cosine(n);
    result = cosine_results[cosine_calls++];
    return result;
}
f32 func_80003E10_4A10(u16 n) {
    f32 result;
    second=n;
    record_trig(1, n);
    if (!use_trig_fixture) return -3.0f;
    if (use_table_fixture) return table_sine(n);
    result = sine_results[sine_calls++];
    return result;
}
f32 _nsqrtf(f32 value) {
    if (sqrt_calls < 3) sqrt_inputs[sqrt_calls] = value;
    sqrt_calls++;
    return sqrtf(value);
}
s32 func_8000E28C_EE8C(f32,f32,f32,f32);
s32 func_8000E630_F230(f32,u16,f32 *,f32 *);
s32 func_8000E39C_EF9C(f32,f32,f32,f32,u8 *);
/* Test-only reference from the ROM trace; the production target stays GLOBAL_ASM. */
static s32 reference_E2D4(f32 scale, u16 angle_a, u16 angle_b, u8 *out) {
    f32 first_scale;
    f32 second_scale;
    f32 sine;

    if (scale < 0.0f) {
        first_scale = -scale;
    } else {
        first_scale = scale;
    }
    sine = func_80003E10_4A10(angle_a);
    *(f32 *)(out + 0x74) = sine * first_scale;

    if (scale < 0.0f) {
        second_scale = -scale;
    } else {
        second_scale = scale;
    }
    second_scale = func_80003EA0_4AA0(angle_a) * second_scale;
    *(f32 *)(out + 0x70) = func_80003E10_4A10(angle_b) * second_scale;
    *(f32 *)(out + 0x78) = func_80003EA0_4AA0(angle_b) * second_scale;
    return 1;
}
typedef struct {
    u8 prefix[0x08];
    f32 x;
    f32 y;
    f32 z;
} TestPosition;
typedef struct {
    u8 prefix[0x18];
    const TestPosition *position;
    u8 gap[0x70 - 0x18 - sizeof(const f32 *)];
    f32 at_70;
    f32 at_74;
    f32 at_78;
} TestTransform;
/* Test-only reference from the ROM trace; compared with checked production C below. */
static s32 reference_E39C(f32 scale, f32 x, f32 y, f32 z, u8 *object) {
    const TestPosition *position = *(const TestPosition **)(object + 0x18);
    volatile f32 dx = x - position->x;
    volatile f32 dy = y - position->y;
    volatile f32 dz = z - position->z;
    volatile f32 dx_squared = dx * dx;
    volatile f32 scale_squared = scale * scale;
    volatile f32 dy_squared = dy * dy;
    volatile f32 dz_squared = dz * dz;
    volatile f32 xy_squared = dx_squared + dy_squared;
    volatile f32 length_squared = xy_squared + dz_squared;
    f32 result;

    result = _nsqrtf((dx_squared * scale_squared) / length_squared);
    if (dx < 0.0f) result = -result;
    *(f32 *)(object + 0x70) = result;

    result = _nsqrtf((dy_squared * scale_squared) / length_squared);
    if (dy < 0.0f) result = -result;
    *(f32 *)(object + 0x74) = result;

    result = _nsqrtf((dz_squared * scale_squared) / length_squared);
    if (dz < 0.0f) result = -result;
    *(f32 *)(object + 0x78) = result;
    return 1;
}
static unsigned float_bits(f32 value) {
    union { f32 f; unsigned u; } bits;
    bits.f = value;
    return bits.u;
}
static s32 check_E39C(f32 scale, f32 x, f32 y, f32 z, u8 *object) {
    TestTransform expected = *(TestTransform *)object;
    f32 expected_sqrt_inputs[3];
    s32 expected_return;
    s32 actual_return;
    unsigned i;

    sqrt_calls = 0;
    expected_return = reference_E39C(scale, x, y, z, (u8 *)&expected);
    assert(sqrt_calls == 3);
    for (i = 0; i < 3; i++) expected_sqrt_inputs[i] = sqrt_inputs[i];

    sqrt_calls = 0;
    actual_return = func_8000E39C_EF9C(scale, x, y, z, object);
    assert(actual_return == expected_return);
    assert(sqrt_calls == 3);
    assert(float_bits(*(f32 *)(object + 0x70)) == float_bits(expected.at_70));
    assert(float_bits(*(f32 *)(object + 0x74)) == float_bits(expected.at_74));
    assert(float_bits(*(f32 *)(object + 0x78)) == float_bits(expected.at_78));
    for (i = 0; i < 3; i++) {
        assert(float_bits(sqrt_inputs[i]) == float_bits(expected_sqrt_inputs[i]));
    }
    return actual_return;
}
static void set_trig_fixture(f32 sine_a, f32 cosine_a, f32 sine_b, f32 cosine_b) {
    sine_results[0] = sine_a;
    sine_results[1] = sine_b;
    cosine_results[0] = cosine_a;
    cosine_results[1] = cosine_b;
    sine_calls = cosine_calls = trig_calls = 0;
    use_trig_fixture = 1;
    use_table_fixture = 0;
}
static void set_table_fixture(void) {
    sine_calls = cosine_calls = trig_calls = 0;
    use_trig_fixture = 1;
    use_table_fixture = 1;
}
static void assert_trig_order(u16 angle_a, u16 angle_b) {
    assert(trig_calls == 4);
    assert(trig_kinds[0] == 1 && trig_angles[0] == angle_a);
    assert(trig_kinds[1] == 2 && trig_angles[1] == angle_a);
    assert(trig_kinds[2] == 1 && trig_angles[2] == angle_b);
    assert(trig_kinds[3] == 2 && trig_angles[3] == angle_b);
}
static void test_zero_and_quadrant_axes(void) {
    TestOutput out;
    unsigned char *base = (unsigned char *)&out;
    unsigned i;
    for (i = 0; i < sizeof(out); i++) base[i] = 0xA5;

    set_trig_fixture(0.0f, 1.0f, 0.0f, 1.0f);
    assert(reference_E2D4(8.0f, 0, 0, base) == 1);
    assert(out.at_70 == 0.0f && out.at_74 == 0.0f && out.at_78 == 8.0f);
    assert_trig_order(0, 0);
    for (i = 0; i < 0x70; i++) assert(base[i] == 0xA5);

    for (i = 0; i < sizeof(out); i++) base[i] = 0xA5;
    set_trig_fixture(1.0f, 0.0f, 0.0f, -1.0f);
    assert(reference_E2D4(3.5f, 0x100, 0x200, base) == 1);
    assert(out.at_70 == 0.0f && out.at_74 == 3.5f);
    assert(float_bits(out.at_78) == 0x80000000U);
    assert_trig_order(0x100, 0x200);
    for (i = 0; i < 0x70; i++) assert(base[i] == 0xA5);
}
static void test_scale_sign_and_signed_zero(void) {
    TestOutput out;
    unsigned char *base = (unsigned char *)&out;
    set_trig_fixture(0.5f, 1.0f, -0.25f, 0.5f);
    assert(reference_E2D4(-5.0f, 12, 34, base) == 1);
    assert(out.at_74 == 2.5f && out.at_70 == -1.25f && out.at_78 == 2.5f);
    assert_trig_order(12, 34);

    set_trig_fixture(1.0f, 1.0f, 1.0f, -1.0f);
    assert(reference_E2D4(-0.0f, 12, 34, base) == 1);
    assert(float_bits(out.at_74) == 0x80000000U);
    assert(float_bits(out.at_70) == 0x80000000U);
    assert(float_bits(out.at_78) == 0x00000000U);
}
static void test_helper_owned_angle_wrap(void) {
    TestOutput out_a, out_b;
    set_table_fixture();
    assert(reference_E2D4(2.0f, 0, 0x100, (u8 *)&out_a) == 1);
    assert_trig_order(0, 0x100);
    set_table_fixture();
    assert(reference_E2D4(2.0f, 0x400, 0x500, (u8 *)&out_b) == 1);
    assert_trig_order(0x400, 0x500);
    assert(float_bits(out_a.at_70) == float_bits(out_b.at_70));
    assert(float_bits(out_a.at_74) == float_bits(out_b.at_74));
    assert(float_bits(out_a.at_78) == float_bits(out_b.at_78));
}
static void test_single_precision_multiply_order(void) {
    TestOutput out;
    set_trig_fixture(0.33333334f, 0.57735026f, -0.12345679f, 0.9876543f);
    assert(reference_E2D4(-7.3f, 17, 29, (u8 *)&out) == 1);
    assert(float_bits(out.at_70) == 0xBF053437U);
    assert(float_bits(out.at_74) == 0x401BBBBCU);
    assert(float_bits(out.at_78) == 0x40853437U);
    assert_trig_order(17, 29);
}
static void test_E39C_float_arguments_and_normalized_output(void) {
    TestTransform target;
    TestPosition position = { { 0 }, 2.5f, -6.25f, 88.0f };
    unsigned char *bytes = (unsigned char *)&target;
    unsigned i;

    assert(offsetof(TestPosition, x) == 0x08);
    assert(offsetof(TestPosition, y) == 0x0C);
    assert(offsetof(TestPosition, z) == 0x10);
    assert(offsetof(TestTransform, position) == 0x18);
    assert(offsetof(TestTransform, at_70) == 0x70);
    assert(offsetof(TestTransform, at_74) == 0x74);
    assert(offsetof(TestTransform, at_78) == 0x78);
    for (i = 0; i < sizeof(target); i++) bytes[i] = 0xA5;
    target.position = &position;
    sqrt_calls = 0;
    assert(check_E39C(26.0f, 5.5f, -2.25f, 100.0f, bytes) == 1);
    assert(target.at_70 == 6.0f && target.at_74 == 8.0f && target.at_78 == 24.0f);
    assert(sqrt_calls == 3);
    assert(float_bits(sqrt_inputs[0]) == float_bits(36.0f));
    assert(float_bits(sqrt_inputs[1]) == float_bits(64.0f));
    assert(float_bits(sqrt_inputs[2]) == float_bits(576.0f));
    for (i = 0; i < 0x70; i++) {
        if (i < 0x18 || i >= 0x18 + sizeof(target.position)) assert(bytes[i] == 0xA5);
    }
}
static void test_E39C_sign_and_signed_zero(void) {
    TestTransform target;
    TestPosition position = { { 0 }, 0.0f, 0.0f, 0.0f };
    target.position = &position;
    sqrt_calls = 0;
    assert(check_E39C(-13.0f, -3.0f, -4.0f, -12.0f, (u8 *)&target) == 1);
    assert(target.at_70 == -3.0f && target.at_74 == -4.0f && target.at_78 == -12.0f);

    sqrt_calls = 0;
    assert(check_E39C(5.0f, -0.0f, 3.0f, 4.0f, (u8 *)&target) == 1);
    assert(float_bits(target.at_70) == 0x00000000U);
    assert(target.at_74 == 3.0f && target.at_78 == 4.0f);
}
static void test_E39C_nan_and_zero_length(void) {
    TestTransform target;
    TestPosition position = { { 0 }, 0.0f, 0.0f, 0.0f };
    target.position = &position;
    sqrt_calls = 0;
    assert(check_E39C(1.0f, NAN, 1.0f, 2.0f, (u8 *)&target) == 1);
    assert(sqrt_calls == 3);
    assert(isnan(target.at_70) && isnan(target.at_74) && isnan(target.at_78));

    sqrt_calls = 0;
    assert(check_E39C(1.0f, 0.0f, 0.0f, 0.0f, (u8 *)&target) == 1);
    assert(sqrt_calls == 3);
    assert(isnan(target.at_70) && isnan(target.at_74) && isnan(target.at_78));
}
static void test_E39C_single_precision_rounding_order(void) {
    TestTransform target;
    TestPosition position = { { 0 }, 0.0f, 0.0f, 0.0f };
    target.position = &position;
    sqrt_calls = 0;
    assert(check_E39C(0.1f, 0.3f, 0.7f, 1.1f, (u8 *)&target) == 1);
    assert(float_bits(target.at_70) == 0x3CB7B08DU);
    assert(sqrt_calls == 3);

    assert(check_E39C(3.7f, -0.7f, 1.3f, 2.9f, (u8 *)&target) == 1);
    assert(float_bits(target.at_70) == 0xBF4BBF4BU);
}
int main(void) {
    f32 a=0,b=0;
    assert(offsetof(TestOutput, at_70) == 0x70);
    assert(offsetof(TestOutput, at_74) == 0x74);
    assert(offsetof(TestOutput, at_78) == 0x78);
    assert(func_8000E28C_EE8C(7,8,2,3)==1023);
    assert(x==5 && y==5);
    assert(func_8000E28C_EE8C(8,3,2,5)==1023);
    assert(x==-2 && y==6);
    test_zero_and_quadrant_axes();
    test_scale_sign_and_signed_zero();
    test_helper_owned_angle_wrap();
    test_single_precision_multiply_order();
    test_E39C_float_arguments_and_normalized_output();
    test_E39C_sign_and_signed_zero();
    test_E39C_nan_and_zero_length();
    test_E39C_single_precision_rounding_order();
    use_trig_fixture = 0;
    use_table_fixture = 0;
    assert(func_8000E630_F230(4,123,&a,&b)==1);
    assert(a==8 && b==-12 && first==123 && second==123);
    return 0;
}
